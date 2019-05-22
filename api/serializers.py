from rest_framework_json_api.serializers import ModelSerializer

from api.models import Book, Author


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'
