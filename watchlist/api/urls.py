from django.urls import path
from watchlist.api.views import MovieListApiView, MovieDetailApiView

urlpatterns = [
   path('list/', MovieListApiView.as_view(), name='movie-list'),
   path('<int:pk>/', MovieDetailApiView.as_view(), name='movie-details')
]