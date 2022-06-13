from rest_framework import serializers

from api.models import Book
from api.serializers.author import AuthorSerializer
from api.serializers.series import SeriesSerializer


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    series = SeriesSerializer(required=False)

    class Meta:
        model = Book
        fields = "__all__"
