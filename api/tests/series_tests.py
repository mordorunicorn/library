import simplejson as json
from django.test import TestCase

from api.models import Series


class SeriesCreateTests(TestCase):
    def test_can_create_a_series(self):
        response = self.client.post('/api/series', self.series_data, 'application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Series.objects.count())

    @property
    def series_data(self):
        return {'data': {'type': 'series', 'attributes': {'name': 'The Lord of the Rings'}}}


class SeriesGetEditTests(TestCase):
    def setUp(self):
        self.series = Series.objects.create(name='The Lord of the Rings')

    def test_can_get_a_series(self):
        response = self.client.get(f'/api/series/{self.series.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.series_data, json.loads(response.content))

    def test_can_edit_a_series(self):
        data = self.series_data
        data['data']['attributes']['name'] = 'The Chronicles of Narnia'
        response = self.client.patch(f'/api/series/{self.series.pk}', data, 'application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            'The Chronicles of Narnia', json.loads(response.content)['data']['attributes']['name']
        )

    @property
    def series_data(self):
        return {
            'data': {
                'id': str(self.series.pk),
                'type': 'series',
                'attributes': {'name': 'The Lord of the Rings'},
            }
        }
