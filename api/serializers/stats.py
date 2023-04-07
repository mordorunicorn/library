from rest_framework import serializers


class ReadStatusSerializer(serializers.Serializer):
    read = serializers.IntegerField()
    unread = serializers.IntegerField()


class StatsSerializer(serializers.Serializer):
    book_count = serializers.IntegerField()
    author_count = serializers.IntegerField()
    series_count = serializers.IntegerField()
    books_by_read_status = ReadStatusSerializer()
