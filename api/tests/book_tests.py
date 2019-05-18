import simplejson as json
from django.test import TestCase

from api.models import Book


class BookTests(TestCase):

    def test_can_create_a_book(self):
        data = {
            'data': {
                'type': 'books',
                'attributes': {
                    'title': 'The Silmarillion',
                    'author': 'J.R.R. Tolkien'
                }
            }
        }
        response = self.client.post('/api/books', data, 'application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Book.objects.count())

    def test_cannot_create_book_without_title(self):
        data = {
            'data': {
                'type': 'books',
                'attributes': {
                    'author': 'Neil Gaiman'
                }
            }
        }
        response = self.client.post('/api/books', data, 'application/vnd.api+json')
        self.assertEqual(400, response.status_code)
        content = json.loads(response.content)
        self.assertEqual('This field is required.', content['errors'][0]['detail'])
        self.assertEqual('/data/attributes/title', content['errors'][0]['source']['pointer'])

    def test_cannot_create_book_without_author(self):
        data = {
            'data': {
                'type': 'books',
                'attributes': {
                    'title': 'Beowulf'
                }
            }
        }
        response = self.client.post('/api/books', data, 'application/vnd.api+json')
        self.assertEqual(400, response.status_code)
        content = json.loads(response.content)
        self.assertEqual('This field is required.', content['errors'][0]['detail'])
        self.assertEqual('/data/attributes/author', content['errors'][0]['source']['pointer'])

    def test_can_edit_a_book(self):
        book = Book.objects.create(title='Dracula', author='Some Guy')
        data = {
            'data': {
                'id': str(book.pk),
                'type': 'books',
                'attributes': {
                    'title': 'Dracula',
                    'author': 'Bram Stoker'
                }
            }
        }
        response = self.client.patch(f'/api/books/{book.pk}', data, 'application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(data, json.loads(response.content))

