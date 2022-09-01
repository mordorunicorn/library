from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Author, Book, Genre, Series, Subgenre


class BookViewSetTests(TestCase):
    url = '/api/books/'

    def setUp(self):
        self.fantasy = Genre.objects.create(name="Fantasy")
        self.high_fantasy = Subgenre.objects.create(genre=self.fantasy, name="High")
        self.urban_fantasy = Subgenre.objects.create(genre=self.fantasy, name="Urban")

        self.gaiman = Author.objects.create(first_name='Neil', last_name='Gaiman')
        self.pratchett = Author.objects.create(first_name='Terry', last_name='Pratchett')
        self.book_one = Book.objects.create(
            title='Good Omens',
            year=1990,
            subgenre=self.urban_fantasy,
            read=True,
        )
        self.book_one.authors.set([self.gaiman, self.pratchett])

        self.tolkien = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.series = Series.objects.create(name='The Lord of the Rings')
        self.book_two = Book.objects.create(
            title='The Two Towers',
            year=1954,
            series=self.series,
            series_num=2,
            subgenre=self.high_fantasy,
        )
        self.book_two.authors.add(self.tolkien)

        self.horror = Genre.objects.create(name="Horror")
        self.paranormal = Subgenre.objects.create(genre=self.horror, name="Paranormal")

        self.stoker = Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book_three = Book.objects.create(
            title='Dracula',
            year=1897,
            subgenre=self.paranormal,
        )
        self.book_three.authors.add(self.stoker)

    def test_can_list_all_books(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.book_one.pk,
                'age_group': self.book_one.age_group,
                'audiobook': False,
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
                'cover_url': self.book_one.cover_url,
                'read': self.book_one.read,
                'series': None,
                'series_num': None,
                'subgenre': {
                    'id': self.urban_fantasy.id,
                    'genre': {
                        'id': self.fantasy.id,
                        'name': self.fantasy.name,
                    },
                    'name': self.urban_fantasy.name,
                },
                'title': self.book_one.title,
                'year': self.book_one.year,
            },
            {
                'id': self.book_two.pk,
                'age_group': self.book_two.age_group,
                'audiobook': False,
                'authors': [
                    {
                        'id': self.tolkien.pk,
                        'first_name': self.tolkien.first_name,
                        'last_name': self.tolkien.last_name,
                    },
                ],
                'cover_url': self.book_two.cover_url,
                'read': self.book_two.read,
                'series': {
                    'id': self.book_two.series.pk,
                    'name': self.book_two.series.name,
                },
                'series_num': self.book_two.series_num,
                'subgenre': {
                    'id': self.high_fantasy.id,
                    'genre': {
                        'id': self.fantasy.id,
                        'name': self.fantasy.name,
                    },
                    'name': self.high_fantasy.name,
                },
                'title': self.book_two.title,
                'year': self.book_two.year,
            },
            {
                'id': self.book_three.pk,
                'age_group': self.book_three.age_group,
                'audiobook': False,
                'authors': [
                    {
                        'id': self.stoker.pk,
                        'first_name': self.stoker.first_name,
                        'last_name': self.stoker.last_name,
                    },
                ],
                'cover_url': self.book_three.cover_url,
                'read': self.book_three.read,
                'series': None,
                'series_num': None,
                'subgenre': {
                    'id': self.paranormal.id,
                    'genre': {
                        'id': self.horror.id,
                        'name': self.horror.name,
                    },
                    'name': self.paranormal.name,
                },
                'title': self.book_three.title,
                'year': self.book_three.year,
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
        response = self.client.get(self.url, data={'genre': 'Fantasy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertCountEqual([b['id'] for b in response.json()], [self.book_one.pk, self.book_two.pk])
        response = self.client.get(self.url, data={'genre': 'Horror'})
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
            'age_group': self.book_one.age_group,
            'audiobook': False,
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
            'cover_url': self.book_one.cover_url,
            'read': self.book_one.read,
            'series': None,
            'series_num': None,
            'subgenre': {
                'id': self.urban_fantasy.id,
                'genre': {
                    'id': self.fantasy.id,
                    'name': self.fantasy.name,
                },
                'name': self.urban_fantasy.name,
            },
            'title': self.book_one.title,
            'year': self.book_one.year,
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
            'age_group': 'adult',
            'authors': [
                {
                    'id': self.tolkien.pk,
                    'first_name': self.tolkien.first_name,
                    'last_name': self.tolkien.last_name,
                }
            ],
            'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg',
            'series': {
                'id': self.series.pk,
                'name': self.series.name,
            },
            'series_num': 1,
            'subgenre': {
                'id': self.high_fantasy.pk,
                'genre': {
                    'id': self.fantasy.pk,
                    'name': self.fantasy.name,
                },
                'name': self.high_fantasy.name,
            },
            'title': 'The Fellowship of the Ring',
            'year': 1954,
        }
        self.client.logout()
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(403, response.status_code)
