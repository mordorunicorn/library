from rest_framework import viewsets

from api.models import Series
from api.serializers import SeriesSerializer


class SeriesViewSet(viewsets.ModelViewSet):

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
