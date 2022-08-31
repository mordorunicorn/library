from rest_framework import serializers

from api.models import Subgenre
from api.serializers.genre import GenreSerializer


class SubgenreSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Subgenre
        fields = '__all__'
