from rest_framework import viewsets

from api.models import Series
from api.permissions import CanPerformWriteAction
from api.serializers import SeriesSerializer


class SeriesViewSet(viewsets.ModelViewSet):

    permission_classes = [CanPerformWriteAction]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
