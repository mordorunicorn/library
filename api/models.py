from django.db import models

from api import utils


class Author(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else '{self.last_name}'

    def __repr__(self):
        return f'Author(first_name={self.first_name}, last_name={self.last_name})'

    def __str__(self):
        return self.display_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    series = models.CharField(max_length=100, null=True, blank=True)
    series_num = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=50, choices=utils.GENRES, default='fiction')
    age_group = models.CharField(max_length=50, choices=utils.AGE_GROUPS, default='adult')
    read = models.BooleanField(default=False)
    cover_url = models.URLField(blank=True, null=True)

    def __repr__(self):
        return f'{self.title} - {self.author}'

    def __str__(self):
        return f'{self.title} - {self.author}'
