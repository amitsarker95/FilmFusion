from rest_framework import serializers 
from watchlist.models import WatchList, StreamPlatform, Review


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = ('watchlist',)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = ['id','title', 'storyLine', 'active', 'created', 'reviews']


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name = 'watch-list-details')
    class Meta:
        model = StreamPlatform
        fields = '__all__'



