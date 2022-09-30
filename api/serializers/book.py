from rest_framework import serializers

from api.models import Book
from api.serializers.author import AuthorSerializer
from api.serializers.series import SeriesSerializer
from api.serializers.subgenre import SubgenreSerializer
from api.serializers.tag import TagSerializer


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    series = SeriesSerializer(required=False)
    subgenre = SubgenreSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"
