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
