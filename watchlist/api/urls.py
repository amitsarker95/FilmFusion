from django.urls import path
from watchlist.api.views import WatchListApiView, WatchListDetailApiView, StreamPlatformApiView, \
                                StreamPlatformDetailApiView , ReviewListView, ReviewDetailView, ReviewCreateView

urlpatterns = [
   path('list/', WatchListApiView.as_view(), name='watch-list'),
   path('<int:pk>/', WatchListDetailApiView.as_view(), name='watch-list-details'),

   path('stream/', StreamPlatformApiView.as_view(), name='stream'),
   path('stream/<int:pk>', StreamPlatformDetailApiView.as_view(), name='stream-detail'),

   path('stream/<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
   path('stream/<int:pk>/review/', ReviewListView.as_view(), name='stream-review-list'),
   path('stream/review/<int:pk>', ReviewDetailView.as_view(), name='review-detail')

   # path('review/', ReviewListView.as_view(), name='review-list'),
   # path('review/<int:pk>', ReviewDetailView.as_view(), name='review-detail'),
]