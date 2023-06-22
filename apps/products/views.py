from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Min, Max
from django.db.models.functions import Coalesce

from .models import Category, Product, Subcategory, Tag, Brand, Rating, Wishlist, Stock
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    SubcategorySerializer, 
    TagSerializer,
    BrandSerializer, 
    RatingSerializer, 
    WishlistSerializer,
    StockSerializer
)

from tools.custom_permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = {
        'category': ['exact'],
        'subcategory': ['exact'],
        'tags': ['exact'],
        'brand': ['exact'],
        'product_stock__price': ['exact', 'gte', 'lte'],
        'discount': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'product_ratings__star': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['name', 'product_stock__price', 'discount', 'created_at', 'product_ratings__star']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset.annotate(
            min_price=Coalesce(Min('product_stock__price'), 0), 
            max_price=Coalesce(Max('product_stock__price'), 0)
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get product stock
        stock = Stock.objects.filter(product=instance)
        stock_serializer = StockSerializer(stock, many=True)

        # get 5 latest ratings with 5 stars
        ratings = Rating.objects.filter(product=instance, star=5).order_by('-created_at')[:5]
        ratings_serializer = RatingSerializer(ratings, many=True)

        # acumulate all ratings
        ratings = Rating.objects.filter(product=instance)
        total_ratings = ratings.count()
        total_stars = sum([rating.star for rating in ratings])

        # calculate average rating
        try:
            average_rating = total_stars / total_ratings
        except ZeroDivisionError:
            average_rating = 0

        # count wishlist
        wishlist = Wishlist.objects.filter(product=instance)
        total_wishlist = wishlist.count()

        # get 5 latest product with same category and brand
        related_products = Product.objects.filter(category=instance.category, brand=instance.brand).exclude(id=instance.id)[:5]

        return Response({
            'product': serializer.data,
            'stock': stock_serializer.data,
            'total_rating': average_rating,
            'latest_rating': ratings_serializer.data,
            'total_wishlist': total_wishlist,
            'related_products': ProductSerializer(related_products, many=True).data
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    lookup_field = 'slug'
    
class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    lookup_field = 'slug'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    lookup_field = 'slug'
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    lookup_field = 'slug'
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'product': ['exact'],
        'star': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['star', 'created_at']
    ordering = ['-created_at']

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'product': ['exact'],
    }
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['product__name']
    filterset_fields = {
        'product': ['exact'],
        'purchase_date': ['exact', 'gte', 'lte'],
        'expiry_date': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['product__name', 'purchase_date', 'expiry_date']
    ordering = ['-purchase_date']
