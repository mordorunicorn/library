from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Author


class AuthorViewSetTests(TestCase):
    url = '/api/authors/'

    def setUp(self):
        self.author = Author.objects.create(first_name='Lucy Maude', last_name='Montgomery')
        user = User.objects.create_user(username='achillz@test.com', password='password')
        assert self.client.login(username=user.username, password='password')

    def test_can_list_all_authors(self):
        author = Author.objects.create(first_name='Neil', last_name='Gaiman')
        response = self.client.get(self.url)
        expected = [
            {
                'id': self.author.pk,
                'first_name': self.author.first_name,
                'last_name': self.author.last_name,
            },
            {
                'id': author.pk,
                'first_name': author.first_name,
                'last_name': author.last_name,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_list_all_authors_when_not_logged_in(self):
        author = Author.objects.create(first_name='Neil', last_name='Gaiman')
        self.client.logout()
        response = self.client.get(self.url)
        expected = [
            {
                'id': self.author.pk,
                'first_name': self.author.first_name,
                'last_name': self.author.last_name,
            },
            {
                'id': author.pk,
                'first_name': author.first_name,
                'last_name': author.last_name,
            },
        ]
        self.assertCountEqual(expected, response.json())

    def test_can_get_an_author(self):
        data = {
            'id': self.author.pk,
            'first_name': 'Lucy Maude',
            'last_name': 'Montgomery',
        }
        response = self.client.get(f'{self.url}{self.author.pk}/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(data, response.json())

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

    def test_cannot_create_author_if_not_logged_in(self):
        data = {
            'last_name': 'Homer',
        }
        self.client.logout()
        response = self.client.post(self.url, data, 'application/json')
        self.assertEqual(403, response.status_code)
