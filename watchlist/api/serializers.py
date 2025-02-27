from rest_framework import serializers 
from watchlist.models import WatchList, StreamPlatform, Review

# Review Start points
class ReviewCreateSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

#Review End 

#----------------------------------------------------------------#


#Watch List Start Points

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = ['id','title', 'storyLine','avg_rating','total_reviews', 'active', 'created','platform']


#Watch List End


#----------------------------------------------------------------#


#Stream Start points

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name = 'watch-list-details')
    class Meta:
        model = StreamPlatform
        fields = '__all__'


#Stream End



