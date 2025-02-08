from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('watchlist/', include('watchlist.api.urls')),
    path('account/', include('user_app.api.urls')),
    
]
