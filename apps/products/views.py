from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, Subcategory, Brand, Rating, Stock
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, SubcategorySerializer, BrandSerializer, RatingSerializer, StockSerializer
from .permissions import IsAdminOrReadOnly, AllowAny

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category__slug', 'subcategory__slug', 'brand__slug']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']


    def get_serializer(self, *args, **kwargs):
        """Use ProductDetailSerializer when retrieving a product"""

        if self.action == 'retrieve':
            return ProductDetailSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """ This method is used to retrieve a product, ratings and its stock """

        instance = self.get_object()
        ratings = Rating.objects.filter(product=instance)
        stock = Stock.objects.filter(product=instance)
        serializer = self.get_serializer(instance)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(ratings, request)
        serializer_ratings = RatingSerializer(result_page, many=True)
        serializer_stock = StockSerializer(stock, many=True)

        return paginator.get_paginated_response({
            'product': serializer.data,
            'ratings': serializer_ratings.data,
            'stock': serializer_stock.data
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
    
    def retrieve(self, request, *args, **kwargs):
        """ This method is used to retrieve a category and its products """
        
        instance = self.get_object()
        products = Product.objects.filter(category__slug=instance.slug)
        serializer = self.get_serializer(instance)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(products, request)
        serializer_products = ProductSerializer(result_page, many=True)

        return paginator.get_paginated_response({
            'category': serializer.data,
            'products': serializer_products.data
        })
    
class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['star']
    ordering_fields = ['star', 'created_at']
    ordering = ['-created_at']
    
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['product__name']
    filterset_fields = ['purchase_date', 'expiry_date']
    ordering_fields = ['product__name', 'purchase_date', 'expiry_date']
    ordering = ['-purchase_date']

