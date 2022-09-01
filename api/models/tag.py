from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
