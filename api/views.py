from rest_framework import generics

from api import models, serializers


class BookListView(generics.ListCreateAPIView):
    resource_name = 'books'
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    resource_name = 'books'
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()
