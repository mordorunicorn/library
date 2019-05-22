from rest_framework import generics

from api import models, serializers


class BookMixin():
    resource_name = 'books'
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()


class BookListView(BookMixin, generics.ListCreateAPIView):
    pass


class BookDetailView(BookMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class AuthorMixin():
    resource_name = 'authors'
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()


class AuthorListView(AuthorMixin, generics.ListCreateAPIView):
    pass


class AuthorDetailView(AuthorMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
