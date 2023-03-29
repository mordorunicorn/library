from django.db import models

from api import utils


class Book(models.Model):
    age_group = models.CharField(max_length=50, choices=utils.AGE_GROUPS, default='adult')
    audiobook = models.BooleanField(default=False)
    authors = models.ManyToManyField('Author', related_name='books')
    cover_url = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    series = models.ForeignKey(
        'Series', related_name='books', on_delete=models.SET_NULL, null=True, blank=True
    )
    series_num = models.IntegerField(null=True, blank=True)
    subgenre = models.ForeignKey('Subgenre', related_name='books', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='books', blank=True)
    year = models.IntegerField()

    @property
    def author_display(self):
        return ', '.join(a.display_name for a in self.authors.all())

    def __repr__(self):
        return f'{self.title} - {self.author_display}'

    def __str__(self):
        return f'{self.title} - {self.author_display}'

    class Meta:
        unique_together = ('title', 'year')
        ordering = ['title']
