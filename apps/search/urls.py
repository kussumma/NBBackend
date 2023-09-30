from django.urls import path
from .views import SearchView, TrendingSearchView

urlpatterns = [
    path("v1/search/", SearchView.as_view(), name="search"),
    path("v1/search/trending/", TrendingSearchView.as_view(), name="trending-search"),
]
