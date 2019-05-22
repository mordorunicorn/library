import simplejson as json
from django.test import TestCase

from api.models import Author


class AuthorCreateTests(TestCase):

    def test_can_create_an_author(self):
        response = self.client.post('/api/authors', self.author_data, 'application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Author.objects.count())

    def test_can_create_author_without_first_name(self):
        data = self.author_data
        del data['data']['attributes']['first_name']
        response = self.client.post('/api/authors', data, 'application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Author.objects.count())

    def test_cannot_create_author_without_last_name(self):
        data = self.author_data
        del data['data']['attributes']['last_name']
        response = self.client.post('/api/authors', data, 'application/vnd.api+json')
        self.assertEqual(400, response.status_code)
        content = json.loads(response.content)
        self.assertEqual('This field is required.', content['errors'][0]['detail'])
        self.assertEqual('/data/attributes/last_name', content['errors'][0]['source']['pointer'])

    @property
    def author_data(self):
        return {
            'data': {
                'type': 'authors',
                'attributes': {
                    'first_name': 'C.S.',
                    'last_name': 'Lewis'
                }
            }
        }


class AuthorGetEditTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='Lucy Maude', last_name='Montgomery')

    def test_can_get_an_author(self):
        response = self.client.get(f'/api/authors/{self.author.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.montgomery_data, json.loads(response.content))

    def test_can_edit_an_author(self):
        data = self.montgomery_data
        data['data']['attributes']['first_name'] = 'Lucy'
        response = self.client.patch(f'/api/authors/{self.author.pk}', data, 'application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Lucy', json.loads(response.content)['data']['attributes']['first_name'])

    @property
    def montgomery_data(self):
        return {
            'data': {
                'id': str(self.author.pk),
                'type': 'authors',
                'attributes': {
                    'first_name': 'Lucy Maude',
                    'last_name': 'Montgomery',
                }
            }
        }
