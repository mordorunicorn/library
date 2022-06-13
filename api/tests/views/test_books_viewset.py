from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Author, Book, Series


class BookViewSetTests(TestCase):
    url = '/api/books/'

    def setUp(self):
        self.gaiman = Author.objects.create(first_name='Neil', last_name='Gaiman')
        self.pratchett = Author.objects.create(first_name='Terry', last_name='Pratchett')
        self.book_one = Book.objects.create(title='Good Omens', year=1990, genre='fantasy', read=True)
        self.book_one.authors.set([self.gaiman, self.pratchett])

        self.tolkien = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.series = Series.objects.create(name='The Lord of the Rings')
        self.book_two = Book.objects.create(
            title='The Two Towers',
            year=1954,
            genre='fantasy',
            series=self.series,
            series_num=2,
        )
        self.book_two.authors.add(self.tolkien)

        self.stoker = Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book_three = Book.objects.create(title='Dracula', year=1897, genre='horror')
        self.book_three.authors.add(self.stoker)

    def test_can_list_all_books(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.book_one.pk,
                'title': self.book_one.title,
                'series_num': None,
                'year': self.book_one.year,
                'genre': self.book_one.genre,
                'age_group': self.book_one.age_group,
                'cover_url': self.book_one.cover_url,
                'series': None,
                'authors': [
                    {
                        'id': self.gaiman.pk,
                        'first_name': self.gaiman.first_name,
                        'last_name': self.gaiman.last_name,
                    },
                    {
                        'id': self.pratchett.pk,
                        'first_name': self.pratchett.first_name,
                        'last_name': self.pratchett.last_name,
                    },
                ],
                'read': self.book_one.read,
            },
            {
                'id': self.book_two.pk,
                'title': self.book_two.title,
                'series_num': self.book_two.series_num,
                'year': self.book_two.year,
                'genre': self.book_two.genre,
                'age_group': self.book_two.age_group,
                'cover_url': self.book_two.cover_url,
                'series': {
                    'id': self.book_two.series.pk,
                    'name': self.book_two.series.name,
                },
                'authors': [
                    {
                        'id': self.tolkien.pk,
                        'first_name': self.tolkien.first_name,
                        'last_name': self.tolkien.last_name,
                    },
                ],
                'read': self.book_two.read,
            },
            {
                'id': self.book_three.pk,
                'title': self.book_three.title,
                'series_num': None,
                'year': self.book_three.year,
                'genre': self.book_three.genre,
                'age_group': self.book_three.age_group,
                'cover_url': self.book_three.cover_url,
                'series': None,
                'authors': [
                    {
                        'id': self.stoker.pk,
                        'first_name': self.stoker.first_name,
                        'last_name': self.stoker.last_name,
                    },
                ],
                'read': self.book_three.read,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_filter_books_by_author(self):
        response = self.client.get(self.url, data={'author_id': self.gaiman.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_one.pk)
        response = self.client.get(self.url, data={'author_id': self.stoker.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_three.pk)

    def test_can_filter_books_by_genre(self):
        response = self.client.get(self.url, data={'genre': 'fantasy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertCountEqual([b['id'] for b in response.json()], [self.book_one.pk, self.book_two.pk])
        response = self.client.get(self.url, data={'genre': 'horror'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_three.pk)

    def test_can_filter_books_by_age_group(self):
        self.book_two.age_group = 'young-adult'
        self.book_two.save()

        response = self.client.get(self.url, data={'age_group': 'adult'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertCountEqual([b['id'] for b in response.json()], [self.book_one.pk, self.book_three.pk])
        response = self.client.get(self.url, data={'age_group': 'young-adult'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_two.pk)

    def test_can_filter_books_by_read(self):
        response = self.client.get(self.url, data={'read': False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertCountEqual([b['id'] for b in response.json()], [self.book_two.pk, self.book_three.pk])
        response = self.client.get(self.url, data={'read': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_one.pk)

    def test_can_filter_books_by_series_id(self):
        response = self.client.get(self.url, data={'series_id': self.series.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], self.book_two.pk)

    def test_can_get_a_specific_book(self):
        response = self.client.get(f'{self.url}{self.book_one.pk}/')
        self.assertEqual(200, response.status_code)
        expected = {
            'id': self.book_one.pk,
            'title': self.book_one.title,
            'series_num': None,
            'year': self.book_one.year,
            'genre': self.book_one.genre,
            'age_group': self.book_one.age_group,
            'cover_url': self.book_one.cover_url,
            'series': None,
            'authors': [
                {
                    'id': self.gaiman.pk,
                    'first_name': self.gaiman.first_name,
                    'last_name': self.gaiman.last_name,
                },
                {
                    'id': self.pratchett.pk,
                    'first_name': self.pratchett.first_name,
                    'last_name': self.pratchett.last_name,
                },
            ],
            'read': self.book_one.read,
        }
        self.assertEqual(expected, response.json())

    def test_can_partial_edit_a_book(self):
        data = {
            'id': self.book_one.pk,
            'read': True,
        }
        user = User.objects.create_user(username='achillz@test.com', password='password')
        assert self.client.login(username=user.username, password='password')
        response = self.client.patch(f'{self.url}{self.book_one.pk}/', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.book_one.refresh_from_db()
        self.assertTrue(self.book_one.read)

    def test_cannot_edit_a_book_if_not_logged_in(self):
        data = {
            'id': self.book_one.pk,
            'read': True,
        }
        self.client.logout()
        response = self.client.patch(f'{self.url}{self.book_one.pk}/', data, 'application/json')
        self.assertEqual(403, response.status_code)

    def test_cannot_create_a_book_if_not_logged_in(self):
        data = {
            'title': 'The Fellowship of the Ring',
            'series_num': 1,
            'year': 1954,
            'genre': 'fantasy',
            'age_group': 'adult',
            'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg',
            'series': {
                'id': self.series.pk,
                'name': self.series.name,
            },
            'authors': [
                {
                    'id': self.tolkien.pk,
                    'first_name': self.tolkien.first_name,
                    'last_name': self.tolkien.last_name,
                }
            ],
        }
        self.client.logout()
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(403, response.status_code)

    # TODO(jpg) add these tests back if they ever become relevant
    # def test_can_create_a_book(self):
    #     data = {
    #         'title': 'The Fellowship of the Ring',
    #         'series_num': 1,
    #         'year': 1954,
    #         'genre': 'fantasy',
    #         'age_group': 'adult',
    #         'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg',
    #         'series': {
    #             'id': self.series.pk,
    #             'name': self.series.name,
    #         },
    #         'authors': [
    #             {
    #                 'id': self.tolkien.pk,
    #                 'first_name': self.tolkien.first_name,
    #                 'last_name': self.tolkien.last_name,
    #             }
    #         ],
    #     }
    #     response = self.client.post(self.url, data, 'application/json')
    #     self.assertEqual(201, response.status_code)
    #     book = Book.objects.get(title='The Fellowship of the Ring')
    #     self.assertEqual('The Fellowship of the Ring', book.title)
    #     self.assertEqual(1, book.series_num)
    #     self.assertEqual(1954, book.year)
    #     self.assertEqual('fantasy', book.genre)
    #     self.assertEqual('adult', book.age_group)
    #     self.assertEqual('https://images.gr-assets.com/books/1419127843l/18510.jpg', book.cover_url)
    #     self.assertEqual(self.series, book.series)
    #     self.assertEqual(self.tolkien, book.authors.first())

    # def test_cannot_create_book_without_a_title(self):
    #     data = {
    #         'year': 1954,
    #         'genre': 'fantasy',
    #         'age_group': 'adult',
    #         'authors': [
    #             {
    #                 'id': self.tolkien.pk,
    #                 'first_name': self.tolkien.first_name,
    #                 'last_name': self.tolkien.last_name,
    #             }
    #         ],
    #     }
    #     response = self.client.post(self.url, data, 'application/json')
    #     self.assertEqual(400, response.status_code)
    #     self.assertEqual({'title': ['This field is required.']}, response.json())

    # def test_can_edit_a_book(self):
    #     data = {
    #         'id': self.book_three.pk,
    #         'title': 'Dracula',
    #         'year': 1999,
    #         'genre': 'horror',
    #         'read': False,
    #         'series_num': None,
    #         'age_group': 'adult',
    #         'cover_url': None,
    #         'authors': [
    #             {
    #                 'id': self.stoker.pk,
    #                 'first_name': self.stoker.first_name,
    #                 'last_name': self.stoker.last_name,
    #             }
    #         ],
    #         'series': None,
    #     }
    #     response = self.client.patch(f'{self.url}{self.book_three.pk}/', data, 'application/json')
    #     print(response.json())
    #     self.assertEqual(200, response.status_code)
    #     self.book_three.refresh_from_db()
    #     self.assertEqual(1999, self.book_three.year)

    # def test_can_edit_a_book_to_have_series(self):
    #     data = {
    #         'id': self.book_three.pk,
    #         'title': 'Dracula',
    #         'year': 1999,
    #         'genre': 'horror',
    #         'read': False,
    #         'series_num': None,
    #         'age_group': 'adult',
    #         'cover_url': None,
    #         'authors': [
    #             {
    #                 'id': self.tolkien.pk,
    #                 'first_name': self.tolkien.first_name,
    #                 'last_name': self.tolkien.last_name,
    #             }
    #         ],
    #         'series': {
    #             'id': self.series.id,
    #             'name': self.series.name,
    #         },
    #     }
    #     response = self.client.patch(f'{self.url}{self.book_three.pk}/', data, 'application/json')
    #     self.assertEqual(200, response.status_code)
    #     self.book_three.refresh_from_db()
    #     self.assertEqual(1999, self.book_three.year)
    #     self.assertEqual(self.series, self.book_three.series)
    #     self.assertEqual([self.stoker], self.book_three.authors.all())
