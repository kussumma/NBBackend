from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    BrandViewSet,
    RatingViewSet,
    StockViewSet
)

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubcategoryViewSet, basename='subcategory')
router.register('brand', BrandViewSet, basename='brand')
router.register('rating', RatingViewSet, basename='rating')
router.register('stock', StockViewSet, basename='stock')

urlpatterns = [
    path('v1/', include(router.urls)),
]