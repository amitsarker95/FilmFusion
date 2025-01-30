from django.urls import path
from watchlist.api.views import WatchListApiView, WatchListDetailApiView, StreamPlatformApiView

urlpatterns = [
   path('list/', WatchListApiView.as_view(), name='watch-list'),
   path('<int:pk>/', WatchListDetailApiView.as_view(), name='watch-list-details'),

   path('stream/', StreamPlatformApiView.as_view(), name='stream')
]