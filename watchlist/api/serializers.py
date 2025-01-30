from rest_framework import serializers 
from watchlist.models import Movies

# def is_valid_description(data):
#     if data['title'] == data['description']:
#         raise serializers.ValidationError("title and description can not be same")
#     return data

class MovieSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movies.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def validate(self, data):
        if data.get('title') == data.get('description'):
            raise serializers.ValidationError("Title and description must be different")
        return data
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("title must be at least 3 characters")
        return value
