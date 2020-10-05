from rest_framework_json_api.serializers import ModelSerializer

from api.models import Series


class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
