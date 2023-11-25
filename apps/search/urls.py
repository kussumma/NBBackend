from django.urls import path
from .views import SearchView, StoreSearchView, TrendingSearchView, SearchHistoryView

urlpatterns = [
    path("v1/search/", SearchView.as_view(), name="search"),
    path("v1/search/store/", StoreSearchView.as_view(), name="store-search"),
    path("v1/search/trending/", TrendingSearchView.as_view(), name="trending-search"),
    path("v1/search/history/", SearchHistoryView.as_view(), name="search-history"),
]
