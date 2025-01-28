from rest_framework import serializers 
from watchlist.models import Movies


class MovieSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movies.objects.create(**validated_data)
