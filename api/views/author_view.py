from rest_framework import viewsets

from api.models import Author
from api.permissions import CanPerformWriteAction
from api.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):

    permission_classes = [CanPerformWriteAction]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
