from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Author, Book, Genre, Series, Subgenre


class SeriesViewSetTests(TestCase):
    url = '/api/series/'

    def setUp(self):
        self.series = Series.objects.create(name='The Lord of the Rings')
        self.fantasy = Genre.objects.create(name='Fantasy')
        self.high_fantasy = Subgenre.objects.create(genre=self.fantasy, name='High')
        self.tolkien = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.two_towers = Book.objects.create(
            title='The Two Towers',
            year=1954,
            series=self.series,
            series_num=2,
            subgenre=self.high_fantasy,
        )
        self.two_towers.authors.add(self.tolkien)
        user = User.objects.create_user(username='achillz@test.com', password='password')
        assert self.client.login(username=user.username, password='password')

    def test_can_list_all_series(self):
        series = Series.objects.create(name='Fruits Basket')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.series.pk,
                'authors': [
                    {
                        'id': self.tolkien.pk,
                        'first_name': self.tolkien.first_name,
                        'last_name': self.tolkien.last_name,
                    },
                ],
                'books': [
                    {
                        'id': self.two_towers.pk,
                        'age_group': self.two_towers.age_group,
                        'audiobook': False,
                        'cover_url': self.two_towers.cover_url,
                        'display_title': self.two_towers.display_title,
                        'is_reading_challenge_eligible': self.two_towers.is_reading_challenge_eligible,
                        'read': self.two_towers.read,
                        'series_num': self.two_towers.series_num,
                        'title': self.two_towers.title,
                        'year': self.two_towers.year,
                    },
                ],
                'name': self.series.name,
            },
            {
                'id': series.pk,
                'authors': [],
                'books': [],
                'name': series.name,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_list_all_series_if_not_logged_in(self):
        series = Series.objects.create(name='Fruits Basket')
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.series.pk,
                'authors': [
                    {
                        'id': self.tolkien.pk,
                        'first_name': self.tolkien.first_name,
                        'last_name': self.tolkien.last_name,
                    },
                ],
                'books': [
                    {
                        'id': self.two_towers.pk,
                        'age_group': self.two_towers.age_group,
                        'audiobook': False,
                        'cover_url': self.two_towers.cover_url,
                        'display_title': self.two_towers.display_title,
                        'is_reading_challenge_eligible': self.two_towers.is_reading_challenge_eligible,
                        'read': self.two_towers.read,
                        'series_num': self.two_towers.series_num,
                        'title': self.two_towers.title,
                        'year': self.two_towers.year,
                    },
                ],
                'name': self.series.name,
            },
            {
                'id': series.pk,
                'authors': [],
                'books': [],
                'name': series.name,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_get_a_specific_series(self):
        fellowship = Book.objects.create(
            title='The Fellowship of the Ring',
            year=1954,
            series=self.series,
            series_num=1,
            subgenre=self.high_fantasy,
        )
        self.two_towers.authors.add(self.tolkien)
        christopher_tolkien = Author.objects.create(first_name='Christopher', last_name='Tolkien')
        self.two_towers.authors.add(christopher_tolkien)
        response = self.client.get(f'{self.url}{self.series.pk}/')
        self.assertEqual(200, response.status_code)
        expected = {
            'id': self.series.pk,
            'authors': [
                {
                    'id': self.tolkien.pk,
                    'first_name': self.tolkien.first_name,
                    'last_name': self.tolkien.last_name,
                },
                {
                    'id': christopher_tolkien.pk,
                    'first_name': christopher_tolkien.first_name,
                    'last_name': christopher_tolkien.last_name,
                },
            ],
            'books': [
                {
                    'id': fellowship.pk,
                    'age_group': fellowship.age_group,
                    'audiobook': False,
                    'cover_url': fellowship.cover_url,
                    'display_title': fellowship.display_title,
                    'is_reading_challenge_eligible': fellowship.is_reading_challenge_eligible,
                    'read': fellowship.read,
                    'series_num': fellowship.series_num,
                    'title': fellowship.title,
                    'year': fellowship.year,
                },
                {
                    'id': self.two_towers.pk,
                    'age_group': self.two_towers.age_group,
                    'audiobook': False,
                    'cover_url': self.two_towers.cover_url,
                    'display_title': self.two_towers.display_title,
                    'is_reading_challenge_eligible': self.two_towers.is_reading_challenge_eligible,
                    'read': self.two_towers.read,
                    'series_num': self.two_towers.series_num,
                    'title': self.two_towers.title,
                    'year': self.two_towers.year,
                },
            ],
            'name': self.series.name,
        }
        self.assertEqual(expected, response.json())

    def test_cannot_create_a_series_if_not_logged_in(self):
        data = {
            'name': 'Anne of Green Gables',
        }
        self.client.logout()
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(403, response.status_code)

    def test_cannot_edit_a_series_if_not_logged_in(self):
        data = {
            'id': self.series.id,
            'name': 'The Chronicles of Narnia',
        }
        self.client.logout()
        response = self.client.patch(f'{self.url}{self.series.pk}/', data, 'application/json')
        self.assertEqual(403, response.status_code)
