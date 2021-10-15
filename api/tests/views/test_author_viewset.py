from django.test import TestCase

from api.models import Author


class AuthorViewSetTests(TestCase):
    url = '/api/authors/'

    def setUp(self):
        self.author = Author.objects.create(first_name='Lucy Maude', last_name='Montgomery')

    def test_can_create_an_author(self):
        data = {
            'first_name': 'C.S.',
            'last_name': 'Lewis',
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(Author.objects.filter(last_name='Lewis').first())

    def test_can_create_author_without_first_name(self):
        data = {
            'last_name': 'Homer',
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(Author.objects.filter(last_name='Homer').first())

    def test_cannot_create_author_without_last_name(self):
        data = {
            'first_name': 'Chewbacca',
        }
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual({'last_name': ['This field is required.']}, response.json())

    def test_can_get_an_author(self):
        data = {
            'id': self.author.pk,
            'first_name': 'Lucy Maude',
            'last_name': 'Montgomery',
        }
        response = self.client.get(f'{self.url}{self.author.pk}/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(data, response.json())

    def test_can_edit_an_author(self):
        data = {
            'id': self.author.pk,
            'first_name': 'Lucy',
            'last_name': 'Montgomery',
        }
        response = self.client.patch(f'{self.url}{self.author.pk}/', data, 'application/json')
        self.assertEqual(200, response.status_code)
        lm = Author.objects.get(last_name='Montgomery')
        self.assertEqual('Lucy', lm.first_name)
