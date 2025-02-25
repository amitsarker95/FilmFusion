from django.shortcuts import get_object_or_404
#Rest Framework
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

#Models , Serializers and Permissions 
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist.models import WatchList, StreamPlatform, Review
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from .serializers import WatchListSerializer, StreamPlatformSerializer, \
                         ReviewSerializer, ReviewCreateSerializer

from .pagination import MyPagination
from .filters import WatchListFilter



#test view for filters
class WList(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_class = WatchListFilter

class WatchListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = WatchList.objects.all().order_by("id")
    serializer_class = WatchListSerializer
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WatchListFilter

    # def list(self, request, *args, **kwargs):
    #     print("🚀 Request Received!")
    #     print("🔍 Raw Request Data:", request.data)
    #     print("Query Parameters:", request.GET)  
    #     filtered_qs = self.filter_queryset(self.get_queryset())
    #     print("Filtered Queryset:", filtered_qs.query) 
    #     print(WatchList.objects.filter(title="Man vs wild"))
    #     print(WatchList.objects.filter(title__icontains="man vs wild"))
    #     return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WatchListDetailApiView(APIView):
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [UserRateThrottle]
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
    permission_classes = [AdminOrReadOnly]
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
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):

        pk = self.kwargs.get('pk')
        watchlist_obj = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        user = Review.objects.filter(watchlist=watchlist_obj, review_user=review_user)

        if user.exists():
            raise ValidationError('You have already reviewed this show.')
        
        if watchlist_obj.total_reviews == 0:
            watchlist_obj.avg_rating = serializer.validated_data['rating']
        else:
            watchlist_obj.avg_rating = (watchlist_obj.avg_rating + serializer.validated_data['rating']) / 2
        watchlist_obj.total_reviews = watchlist_obj.total_reviews + 1
        watchlist_obj.save()
        serializer.save(watchlist=watchlist_obj, review_user=review_user)


class ReviewListView(generics.ListAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = MyPagination
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'active']
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk).order_by('-created')
    
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle]



class UserReviews(generics.ListAPIView):

    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)
    

class UserReviewPerams(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = Review.objects.filter(review_user__username=username)
        return queryset


class WatchListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = WatchList.objects.all().order_by("id")
    serializer_class = WatchListSerializer
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    pagination_class = MyPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




