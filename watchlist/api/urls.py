from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist.api.views import WatchListViewSet, WatchListDetailApiView, \
                                ReviewListView, ReviewDetailView, ReviewCreateView, \
                                StreamPlatformViewSet, UserReviews

router = DefaultRouter()
router.register('stream', StreamPlatformViewSet, basename='stream')
router.register('list', WatchListViewSet, basename='watch-list')


urlpatterns = [
   path('<int:pk>/', WatchListDetailApiView.as_view(), name='watch-list-details'),
   path('', include(router.urls)),
   path('<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
   path('<int:pk>/reviews/', ReviewListView.as_view(), name='stream-review-list'),
   path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
   path('reviews/<str:username>/', UserReviews.as_view(), name='user-reviews'),

]