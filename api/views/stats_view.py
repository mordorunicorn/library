from django.db.models.query import QuerySet

from rest_framework import views
from rest_framework.response import Response

from api import models
from api.serializers import StatsSerializer


class StatsView(views.APIView):

    serializer_class = StatsSerializer

    def get(self, request):
        read_books = [
            book for book in models.Book.objects.filter(read=True) if book.is_reading_challenge_eligible
        ]
        unread_books = [
            book for book in models.Book.objects.filter(read=False) if book.is_reading_challenge_eligible
        ]
        data = self.serializer_class(
            {
                'book_count': models.Book.objects.count(),
                'author_count': models.Author.objects.count(),
                'series_count': models.Series.objects.count(),
                'books_by_read_status': {
                    'read': len(read_books),
                    'unread': len(unread_books),
                },
            }
        )
        return Response(data.data)
