from django.db import models


class Subgenre(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ForeignKey('Genre', related_name='subgenres', on_delete=models.CASCADE)
    exclude_from_challenge = models.BooleanField(default=False)

    def __repr__(self):
        return f'{self.genre.name} > {self.name}'

    def __str__(self):
        return f'{self.genre.name} > {self.name}'

    class Meta:
        ordering = ['genre__name', 'name']
