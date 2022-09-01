from django_filters import rest_framework as filters
from rest_framework import viewsets

from api.models import Book
from api.permissions import CanPerformWriteAction
from api.serializers import BookSerializer


class BookFilter(filters.FilterSet):
    age_group = filters.CharFilter()
    author_id = filters.NumberFilter(method='filter_author_id')
    genre = filters.CharFilter(method='filter_genre')
    read = filters.BooleanFilter()
    series_id = filters.NumberFilter()

    def filter_author_id(self, queryset, name, value):
        return queryset.filter(authors__id=value)

    def filter_genre(self, queryset, name, value):
        return queryset.filter(subgenre__genre__name__iexact=value)


class BookViewSet(viewsets.ModelViewSet):

    filterset_class = BookFilter
    permission_classes = [CanPerformWriteAction]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
