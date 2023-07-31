from django.db import models


class Series(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def authors(self):
        authors = set()
        for book in self.books.all():
            authors.update(book.authors.all())
        return authors

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['name']
