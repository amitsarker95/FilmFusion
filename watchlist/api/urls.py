from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist.api.views import WatchListApiView, WatchListDetailApiView, \
                                ReviewListView, ReviewDetailView, ReviewCreateView, \
                                StreamPlatformViewSet

router = DefaultRouter()
router.register('stream', StreamPlatformViewSet, basename='stream')

urlpatterns = [
   path('list/', WatchListApiView.as_view(), name='watch-list'),
   path('<int:pk>/', WatchListDetailApiView.as_view(), name='watch-list-details'),

   path('', include(router.urls)),

   # path('stream/', StreamPlatformApiView.as_view(), name='stream'),
   # path('stream/<int:pk>', StreamPlatformDetailApiView.as_view(), name='stream-detail'),

   path('<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
   path('<int:pk>/reviews/', ReviewListView.as_view(), name='stream-review-list'),
   path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail')

   # path('review/', ReviewListView.as_view(), name='review-list'),
   # path('review/<int:pk>', ReviewDetailView.as_view(), name='review-detail'),
]