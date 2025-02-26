from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist.api.views import WatchListViewSet, WatchListDetailApiView, \
                                ReviewListView, ReviewDetailView, ReviewCreateView, \
                                StreamPlatformViewSet, UserReviews, UserReviewPerams, WList

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
   path('reviews/', UserReviewPerams.as_view(), name='user-reviews-detail'),
   #test urls for filter
   path('search/', WList.as_view(), name='search'),

]


# from rest_framework.test import APIRequestFactory
# from watchlist.api.views import WatchListViewSet

# factory = APIRequestFactory()
# request = factory.get('/watch/list/')  # Simulating a GET request
# view = WatchListViewSet.as_view({'get': 'list'})  # Binding GET to `list()`

# response = view(request)

# print("✅ Response Status Code:", response.status_code)
# print("✅ Response Data:", response.data)