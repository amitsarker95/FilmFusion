from django_filters import rest_framework as filters
from watchlist.models import WatchList

class WatchListFilter(filters.FilterSet) :
    platform_name = filters.CharFilter(field_name='platform__name', lookup_expr='icontains')
    class Meta:
        model = WatchList
        fields = ['title', 'platform_name', 'avg_rating']