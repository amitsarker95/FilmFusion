from django.urls import path
from watchlist.api.views import WatchListApiView, WatchListDetailApiView, StreamPlatformApiView, \
   StreamPlatformDetailApiView , ReviewListView

urlpatterns = [
   path('list/', WatchListApiView.as_view(), name='watch-list'),
   path('<int:pk>/', WatchListDetailApiView.as_view(), name='watch-list-details'),

   path('stream/', StreamPlatformApiView.as_view(), name='stream'),
   path('stream/<int:pk>', StreamPlatformDetailApiView.as_view(), name='stream-detail'),
   path('review/', ReviewListView.as_view(), name='review-list')
]