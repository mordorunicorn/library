import simplejson as json
from django.test import TestCase

from api.models import Author, Book


class BookCreateTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='J.R.R.', last_name='Tolkien')

    def test_can_create_a_book(self):
        response = self.client.post('/api/books', self.book_data, 'application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Book.objects.count())

    def test_cannot_create_book_without_title(self):
        data = self.book_data
        del data['data']['attributes']['title']
        response = self.client.post('/api/books', data, 'application/vnd.api+json')
        self.assertEqual(400, response.status_code)
        content = json.loads(response.content)
        self.assertEqual('This field is required.', content['errors'][0]['detail'])
        self.assertEqual('/data/attributes/title', content['errors'][0]['source']['pointer'])

    @property
    def book_data(self):
        return {
            'data': {
                'type': 'books',
                'attributes': {
                    'title': 'The Fellowship of the Ring',
                    'series': 'The Lord of the Rings',
                    'series_num': 1,
                    'year': 1954,
                    'genre': 'fantasy',
                    'age_group': 'adult',
                    'cover_url': 'https://images.gr-assets.com/books/1419127843l/18510.jpg'
                },
                'relationships': {
                    'authors': {
                        'data': [
                            {
                                'type': 'authors',
                                'id': self.author.pk
                            }
                        ]
                    }
                }
            }
        }


class BookGetEditTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book = Book.objects.create(title='Dracula', year=1897, genre='horror')
        self.book.authors.set([self.author])
        self.book.save()

    def test_can_get_a_book(self):
        response = self.client.get(f'/api/books/{self.book.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.dracula_data, json.loads(response.content))

    def test_can_edit_a_book(self):
        data = self.dracula_data
        data['data']['attributes']['year'] = 1999
        response = self.client.patch(f'/api/books/{self.book.pk}', data, 'application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1999, json.loads(response.content)['data']['attributes']['year'])

    @property
    def dracula_data(self):
        return {
            'data': {
                'id': str(self.book.pk),
                'type': 'books',
                'attributes': {
                    'title': 'Dracula',
                    'year': 1897,
                    'genre': 'horror',
                    'read': False,
                    'series': None,
                    'series_num': None,
                    'age_group': 'adult',
                    'cover_url': None
                },
                'relationships': {
                    'authors': {
                        'data': [
                            {'type': 'authors', 'id': str(self.author.pk)}
                        ],
                        'meta': {'count': 1}
                    }
                }
            }
        }
