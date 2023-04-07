from django.test import TestCase

from api import models


class SeriesViewSetTests(TestCase):
    url = '/api/stats/'

    def setUp(self):
        self.favorites = models.Tag.objects.create(name='favorites')
        self.fantasy = models.Genre.objects.create(name='Fantasy')
        self.high_fantasy = models.Subgenre.objects.create(genre=self.fantasy, name='High')
        self.urban_fantasy = models.Subgenre.objects.create(genre=self.fantasy, name='Urban')

        self.gaiman = models.Author.objects.create(first_name='Neil', last_name='Gaiman')
        self.pratchett = models.Author.objects.create(first_name='Terry', last_name='Pratchett')
        self.book_one = models.Book.objects.create(
            title='Good Omens',
            year=1990,
            subgenre=self.urban_fantasy,
            read=True,
        )
        self.book_one.authors.set([self.gaiman, self.pratchett])

        self.tolkien = models.Author.objects.create(first_name='J.R.R.', last_name='Tolkien')
        self.series = models.Series.objects.create(name='The Lord of the Rings')
        self.book_two = models.Book.objects.create(
            title='The Two Towers',
            year=1954,
            series=self.series,
            series_num=2,
            subgenre=self.high_fantasy,
        )
        self.book_two.authors.add(self.tolkien)
        self.book_two.tags.add(self.favorites)

        self.horror = models.Genre.objects.create(name='Horror')
        self.paranormal = models.Subgenre.objects.create(genre=self.horror, name='Paranormal')

        self.stoker = models.Author.objects.create(first_name='Bram', last_name='Stoker')
        self.book_three = models.Book.objects.create(
            title='Dracula',
            year=1897,
            subgenre=self.paranormal,
        )
        self.book_three.authors.add(self.stoker)
        self.book_three.tags.add(self.favorites)

    def test_lists_all_stats(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = {
            'book_count': 3,
            'author_count': 4,
            'series_count': 1,
            'books_by_read_status': {
                'read': 1,
                'unread': 2,
            },
        }
        self.assertEqual(expected, response.json())

    def test_read_status_does_not_inclue_childrens_or_middle_grade_books(self):
        models.Book.objects.create(
            title='Roverandom',
            year=1998,
            subgenre=self.high_fantasy,
            age_group='middle-grade',
            read=True,
        )

        picture_book = models.Genre.objects.create(name='Picture Book')
        story_book = models.Subgenre.objects.create(genre=picture_book, name='Story Book')
        models.Book.objects.create(
            title='101 Dalmations',
            year=1961,
            subgenre=story_book,
            age_group='children',
        )
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = {
            'read': 1,
            'unread': 2,
        }
        self.assertEqual(expected, response.json()['books_by_read_status'])

    def test_read_status_does_not_inclue_aticus_tags(self):
        one_piece = models.Book.objects.create(
            title='One Piece Vol. 1',
            year=1997,
            subgenre=self.high_fantasy,
            age_group='adult',
            read=True,
        )
        one_piece.tags.add(models.Tag.objects.create(name='aticus-picks'))

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = {
            'read': 1,
            'unread': 2,
        }
        self.assertEqual(expected, response.json()['books_by_read_status'])

    def test_includes_middle_grade_and_aticus_books_if_series_started(self):
        one_piece_series = models.Series.objects.create(name='One Piece')
        one_piece_one = models.Book.objects.create(
            title='One Piece Vol. 1',
            year=1997,
            series=one_piece_series,
            subgenre=self.high_fantasy,
            age_group='adult',
            read=True,
        )
        one_piece_one.tags.add(models.Tag.objects.create(name='aticus-picks'))

        one_piece_two = models.Book.objects.create(
            title='One Piece Vol. 2',
            year=1997,
            series=one_piece_series,
            subgenre=self.high_fantasy,
            age_group='adult',
            read=False,
        )
        one_piece_two.tags.add(models.Tag.objects.create(name='aticus-picks'))

        sci_fi = models.Genre.objects.create(name='Sci-Fi')
        dystopian = models.Subgenre.objects.create(genre=sci_fi, name='Dystopian')

        shadow_children = models.Series.objects.create(name='Shadow Children')
        models.Book.objects.create(
            title='Among The Hidden',
            year=1998,
            series=shadow_children,
            subgenre=dystopian,
            age_group='middle-grade',
            read=True,
        )
        models.Book.objects.create(
            title='Among The Imposters',
            year=1998,
            series=shadow_children,
            subgenre=dystopian,
            age_group='middle-grade',
            read=False,
        )

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        expected = {
            'read': 3,
            'unread': 4,
        }
        self.assertEqual(expected, response.json()['books_by_read_status'])
