from rest_framework import serializers 
from watchlist.models import WatchList, StreamPlatform



class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ['id','title', 'storyLine', 'active', 'created']


class StreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = '__all__'



