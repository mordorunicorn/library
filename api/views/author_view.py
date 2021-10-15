from rest_framework import viewsets

from api.models import Author
from api.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
