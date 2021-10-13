from django.test import TestCase

from api.models import Series


class SeriesCreateTests(TestCase):
    def test_can_create_a_series(self):
        response = self.client.post('/api/series', self.series_data, 'application/json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Series.objects.count())

    @property
    def series_data(self):
        return {
            'name': 'The Lord of the Rings',
        }


class SeriesGetEditTests(TestCase):
    def setUp(self):
        self.series = Series.objects.create(name='The Lord of the Rings')

    def test_can_get_a_series(self):
        response = self.client.get(f'/api/series/{self.series.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.series_data, response.json())

    def test_can_edit_a_series(self):
        data = self.series_data
        data['name'] = 'The Chronicles of Narnia'
        response = self.client.patch(f'/api/series/{self.series.pk}', data, 'application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('The Chronicles of Narnia', response.json()['name'])

    @property
    def series_data(self):
        return {
            'id': self.series.pk,
            'name': 'The Lord of the Rings',
        }
