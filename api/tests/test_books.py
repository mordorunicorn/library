from django.test import TestCase

from api.models import Author, Book, Series


class BookCreateTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.series = Series.objects.create(name='The Lord of the Rings')

    def test_can_create_a_book(self):
        response = self.client.post('/api/books', self.book_data, 'application/json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Book.objects.count())
        self.assertEqual(1, Book.objects.all()[0].authors.count())

    def test_cannot_create_book_without_a_title(self):
        data = self.book_data
        del data['title']
        response = self.client.post('/api/books', data, 'application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual({'title': ['This field is required.']}, response.json())

    @property
    def book_data(self):
        return {
            'title': 'The Fellowship of the Ring',
            'series_num': 1,
            'year': 1954,
            'genre': 'fantasy',
            'age_group': 'adult',
            'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg',
            'series': self.series.pk,
            'authors': [self.author.pk],
        }


class BookGetEditTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book = Book.objects.create(title='Dracula', year=1897, genre='horror')
        self.book.authors.set([self.author])
        self.book.save()

    def test_can_get_a_book(self):
        response = self.client.get(f'/api/books/{self.book.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.dracula_data, response.json())

    def test_can_edit_a_book(self):
        data = self.dracula_data
        data['year'] = 1999
        response = self.client.patch(f'/api/books/{self.book.pk}', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1999, response.json()['year'])

    @property
    def dracula_data(self):
        return {
            'id': self.book.pk,
            'title': 'Dracula',
            'year': 1897,
            'genre': 'horror',
            'read': False,
            'series_num': None,
            'age_group': 'adult',
            'cover_url': None,
            'authors': [self.author.pk],
            'series': None,
        }
