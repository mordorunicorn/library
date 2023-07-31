from rest_framework import serializers

from api.models import Book


class BasicBookSerializer(serializers.ModelSerializer):
    display_title = serializers.CharField()
    is_reading_challenge_eligible = serializers.BooleanField()

    class Meta:
        model = Book
        exclude = [
            "authors",
            "series",
            "subgenre",
            "tags",
        ]
