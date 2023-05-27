from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Subcategory, Tag, Brand, Rating, Stock
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    SubcategorySerializer, 
    TagSerializer,
    BrandSerializer, 
    RatingSerializer, 
    StockSerializer
)
from .permissions import IsAdminOrReadOnly, AllowAny

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category__slug', 'subcategory__slug', 'brand__slug']
    ordering_fields = ['name', 'price', 'created_at', 'product_ratings__star']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get product ratings
        ratings = Rating.objects.filter(product=instance)

        # enable filters.OrderingFilter on ratings
        ordering = request.query_params.get('ordering', None)
        if ordering:
            if ordering.startswith('-'):
                field = ordering[1:]
                reverse = True
            else:
                field = ordering
                reverse = False

            # apply ordering to ratings queryset
            if field in ['star', 'created_at']:
                ratings = ratings.order_by(ordering)
            else:
                ratings = ratings.order_by('-star')
        else:
            ratings = ratings.order_by('-star')

        # add pagination to ratings
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_ratings = paginator.paginate_queryset(ratings, request)
        ratings_serializer = RatingSerializer(paginated_ratings, many=True)
        
        # get product stock
        stock = Stock.objects.filter(product=instance)
        stock_serializer = StockSerializer(stock, many=True)

        return Response({
            'product': serializer.data,
            'ratings': ratings_serializer.data,
            'stock': stock_serializer.data,
            'ratings_pagination': {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'num_pages': paginator.page.paginator.num_pages,
            }
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
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get category products
        products = Product.objects.filter(category=instance)

        # enable filters.OrderingFilter on products
        ordering = request.query_params.get('ordering', None)
        if ordering:
            if ordering.startswith('-'):
                field = ordering[1:]
                reverse = True
            else:
                field = ordering
                reverse = False

            # apply ordering to products queryset
            if field in ['name', 'price', 'created_at', 'product_ratings__star']:
                products = products.order_by(ordering)
            else:
                products = products.order_by('-created_at')
        else:
            products = products.order_by('-created_at')

        # add pagination to products
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)
        products_serializer = ProductSerializer(paginated_products, many=True)

        return Response({
            'category': serializer.data,
            'products': products_serializer.data,
            'products_pagination': {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'num_pages': paginator.page.paginator.num_pages,
            }
        })
    
class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get subcategory products
        products = Product.objects.filter(subcategory=instance)

        # enable filters.OrderingFilter on products
        ordering = request.query_params.get('ordering', None)
        if ordering:
            if ordering.startswith('-'):
                field = ordering[1:]
                reverse = True
            else:
                field = ordering
                reverse = False

            # apply ordering to products queryset
            if field in ['name', 'price', 'created_at', 'product_ratings__star']:
                products = products.order_by(ordering)
            else:
                products = products.order_by('-created_at')
        else:
            products = products.order_by('-created_at')

        # add pagination to products
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)
        products_serializer = ProductSerializer(paginated_products, many=True)

        return Response({
            'subcategory': serializer.data,
            'products': products_serializer.data,
            'products_pagination': {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'num_pages': paginator.page.paginator.num_pages,
            }
        })

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get brand products
        products = Product.objects.filter(brand=instance)

        # enable filters.OrderingFilter on products
        ordering = request.query_params.get('ordering', None)
        if ordering:
            if ordering.startswith('-'):
                field = ordering[1:]
                reverse = True
            else:
                field = ordering
                reverse = False

            # apply ordering to products queryset
            if field in ['name', 'price', 'created_at', 'product_ratings__star']:
                products = products.order_by(ordering)
            else:
                products = products.order_by('-created_at')
        else:
            products = products.order_by('-created_at')

        # add pagination to products
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)
        products_serializer = ProductSerializer(paginated_products, many=True)

        return Response({
            'brand': serializer.data,
            'products': products_serializer.data,
            'products_pagination': {
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'count': paginator.page.paginator.count,
                'num_pages': paginator.page.paginator.num_pages,
            }
        })
    
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
