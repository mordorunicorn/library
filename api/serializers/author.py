from rest_framework_json_api.serializers import ModelSerializer

from api.models import Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
