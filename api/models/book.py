from django.db import models

from api import utils


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("Author", related_name="books")
    year = models.IntegerField()
    series = models.ForeignKey(
        "Series", related_name="books", on_delete=models.SET_NULL, null=True, blank=True
    )
    series_num = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=50, choices=utils.GENRES, default="fiction")
    age_group = models.CharField(max_length=50, choices=utils.AGE_GROUPS, default="adult")
    read = models.BooleanField(default=False)
    cover_url = models.URLField(blank=True, null=True)

    @property
    def author_display(self):
        return ",".join(a.display_name for a in self.authors.all())

    def __repr__(self):
        return f"{self.title} - {self.author_display}"

    def __str__(self):
        return f"{self.title} - {self.author_display}"
