from rest_framework import serializers

from api.models import Series
from api.serializers.author import AuthorSerializer
from api.serializers.basic_book import BasicBookSerializer


class BasicSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    books = BasicBookSerializer(many=True)

    class Meta:
        model = Series
        fields = '__all__'
