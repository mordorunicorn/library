from django.test import TestCase

from api.models import Author, Book, Series


class BookViewSetTests(TestCase):
    url = '/api/books/'

    def setUp(self):
        self.tolkien = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.series = Series.objects.create(name='The Lord of the Rings')
        self.stoker = Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book = Book.objects.create(title='Dracula', year=1897, genre='horror')
        self.book.authors.set([self.stoker])
        self.book.save()

    def test_can_list_all_books(self):
        series = Series.objects.create(name='Twisted Tales')
        book = Book.objects.create(title='Go the Distance', year=2021, genre='fantasy', series=series)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.book.pk,
                'title': self.book.title,
                'series_num': self.book.series_num,
                'year': self.book.year,
                'genre': self.book.genre,
                'age_group': self.book.age_group,
                'cover_url': self.book.cover_url,
                'series': self.book.series,
                'authors': [self.stoker.pk],
                'read': self.book.read,
            },
            {
                'id': book.pk,
                'title': book.title,
                'series_num': None,
                'year': book.year,
                'genre': book.genre,
                'age_group': book.age_group,
                'cover_url': book.cover_url,
                'series': book.series.pk,
                'authors': [],
                'read': book.read,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_get_a_specific_book(self):
        response = self.client.get(f'{self.url}{self.book.pk}/')
        self.assertEqual(200, response.status_code)
        expected = {
            'id': self.book.pk,
            'title': 'Dracula',
            'year': 1897,
            'genre': 'horror',
            'read': False,
            'series_num': None,
            'age_group': 'adult',
            'cover_url': None,
            'authors': [self.stoker.pk],
            'series': None,
        }
        self.assertEqual(expected, response.json())

    def test_can_create_a_book(self):
        data = {
            'title': 'The Fellowship of the Ring',
            'series_num': 1,
            'year': 1954,
            'genre': 'fantasy',
            'age_group': 'adult',
            'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg',
            'series': self.series.pk,
            'authors': [self.tolkien.pk],
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(201, response.status_code)
        book = Book.objects.get(title='The Fellowship of the Ring')
        self.assertEqual('The Fellowship of the Ring', book.title)
        self.assertEqual(1, book.series_num)
        self.assertEqual(1954, book.year)
        self.assertEqual('fantasy', book.genre)
        self.assertEqual('adult', book.age_group)
        self.assertEqual('https://images.gr-assets.com/books/1419127843l/18510.jpg', book.cover_url)
        self.assertEqual(self.series, book.series)
        self.assertEqual(self.tolkien, book.authors.first())

    def test_cannot_create_book_without_a_title(self):
        data = {
            'year': 1954,
            'genre': 'fantasy',
            'age_group': 'adult',
            'authors': [self.tolkien.pk],
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual({'title': ['This field is required.']}, response.json())

    def test_can_edit_a_book(self):
        data = {
            'id': self.book.pk,
            'title': 'Dracula',
            'year': 1999,
            'genre': 'horror',
            'read': False,
            'series_num': None,
            'age_group': 'adult',
            'cover_url': None,
            'authors': [self.stoker.pk],
            'series': None,
        }
        response = self.client.patch(f'{self.url}{self.book.pk}/', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.book.refresh_from_db()
        self.assertEqual(1999, self.book.year)

    def test_can_partial_edit_a_book(self):
        data = {
            'id': self.book.pk,
            'read': True,
        }
        response = self.client.patch(f'{self.url}{self.book.pk}/', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.book.refresh_from_db()
        self.assertTrue(self.book.read)
