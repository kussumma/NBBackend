from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    SubsubcategoryViewset,
    BrandViewSet,
    RatingViewSet,
    WishlistViewSet,
    StockViewSet
)

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubcategoryViewSet, basename='subcategory')
router.register('subsubcategory', SubsubcategoryViewset, basename='subsubcategory')
router.register('brand', BrandViewSet, basename='brand')
router.register('rating', RatingViewSet, basename='rating')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('stock', StockViewSet, basename='stock')

urlpatterns = [
    path('v1/', include(router.urls)),
]