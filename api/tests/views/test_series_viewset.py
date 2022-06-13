from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Series


class SeriesViewSetTests(TestCase):
    url = '/api/series/'

    def setUp(self):
        self.series = Series.objects.create(name='The Lord of the Rings')
        user = User.objects.create_user(username='achillz@test.com', password='password')
        assert self.client.login(username=user.username, password='password')

    def test_can_list_all_series(self):
        series = Series.objects.create(name='Fruits Basket')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': self.series.pk,
                'name': self.series.name,
            },
            {
                'id': series.pk,
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
                'name': self.series.name,
            },
            {
                'id': series.pk,
                'name': series.name,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_get_a_specific_series(self):
        response = self.client.get(f'{self.url}{self.series.pk}/')
        self.assertEqual(200, response.status_code)
        expected = {
            'id': self.series.pk,
            'name': 'The Lord of the Rings',
        }
        self.assertEqual(expected, response.json())

    def test_can_create_a_series(self):
        data = {
            'name': 'Anne of Green Gables',
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(Series.objects.filter(name='Anne of Green Gables').first())

    def test_can_edit_a_series(self):
        data = {
            'id': self.series.id,
            'name': 'The Chronicles of Narnia',
        }
        response = self.client.patch(f'{self.url}{self.series.pk}/', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('The Chronicles of Narnia', response.json()['name'])

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
