from django.shortcuts import get_object_or_404
#Rest Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
#Models and Serializers
from watchlist.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, \
                         ReviewSerializer, ReviewCreateSerializer


class WatchListApiView(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailApiView(APIView):

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response({'delete': "Object has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class StreamPlatformViewSet(ViewSet):
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response({'delete': "Object has been deleted"}, status=status.HTTP_204_NO_CONTENT)




class ReviewCreateView(generics.CreateAPIView):

    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist_obj = WatchList.objects.get(pk=pk)
        serializer.save(watchlist=watchlist_obj)

class ReviewListView(generics.ListAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk) 
    
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    


