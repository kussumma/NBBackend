from rest_framework import viewsets, views, permissions
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Min, Max, Sum, F
from django.db.models.functions import Coalesce
from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from .models import (
    Category,
    Product,
    Subcategory,
    Subsubcategory,
    Brand,
    Rating,
    Wishlist,
    Stock,
    ExtraProductImage,
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SubcategorySerializer,
    SubsubcategorySerializer,
    BrandSerializer,
    RatingSerializer,
    WishlistSerializer,
    StockSerializer,
    ExtraProductImageSerializer,
)

from tools.custom_permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "product_stock__sku", "description"]
    filterset_fields = {
        "category__slug": ["exact"],
        "subcategory__slug": ["exact"],
        "subsubcategory__slug": ["exact"],
        "brand__slug": ["exact"],
        "brand__name": ["istartswith"],
        "name": ["istartswith"],
        "product_stock__price": ["exact", "gte", "lte"],
        "product_stock__discount": ["exact", "gte", "lte"],
        "created_at": ["exact", "gte", "lte"],
        "product_ratings__star": ["exact", "gte", "lte"],
    }
    ordering_fields = [
        "name",
        "product_stock__price",
        "product_stock__discount",
        "created_at",
        "product_ratings__star",
    ]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset.annotate(
            min_price=Coalesce(Min("product_stock__price"), 0),
            max_price=Coalesce(Max("product_stock__price"), 0),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get product images
        images = ExtraProductImage.objects.filter(product=instance)
        images_serializer = ExtraProductImageSerializer(images, many=True)

        # get product stock
        stock = Stock.objects.filter(product=instance)
        stock_serializer = StockSerializer(stock, many=True)

        # get 5 latest ratings
        ratings = Rating.objects.filter(product=instance).order_by("-created_at")[:5]
        ratings_serializer = RatingSerializer(ratings, many=True)

        # get 3 ratings with >= 4 stars
        highest_ratings = Rating.objects.filter(product=instance, star__gte=4).order_by(
            "-star", "-created_at"
        )[:3]
        highest_ratings_serializer = RatingSerializer(highest_ratings, many=True)

        # get 3 ratings with <= 3 stars
        lowest_ratings = Rating.objects.filter(product=instance, star__lte=3).order_by(
            "-star", "-created_at"
        )[:3]
        lowest_ratings_serializer = RatingSerializer(lowest_ratings, many=True)

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
        related_products = Product.objects.filter(
            category=instance.category, brand=instance.brand
        ).exclude(id=instance.id)[:5]

        return Response(
            {
                "product": serializer.data,
                "images": images_serializer.data,
                "stock": stock_serializer.data,
                "total_rating": average_rating,
                "latest_rating": ratings_serializer.data,
                "highest_rating": highest_ratings_serializer.data,
                "lowest_rating": lowest_ratings_serializer.data,
                "total_wishlist": total_wishlist,
                "related_products": ProductSerializer(related_products, many=True).data,
            }
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    lookup_field = "slug"


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    lookup_field = "slug"


class SubsubcategoryViewset(viewsets.ModelViewSet):
    queryset = Subsubcategory.objects.all()
    serializer_class = SubsubcategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    lookup_field = "slug"


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]
    filterset_fields = {
        "name": ["exact", "istartswith"],
    }
    ordering_fields = ["name"]
    ordering = ["name"]
    lookup_field = "slug"


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        "product": ["exact"],
        "star": ["exact", "gte", "lte"],
    }
    ordering_fields = ["star", "created_at"]
    ordering = ["-created_at"]

    def create(self, request, *args, **kwargs):
        # get product
        product_id = request.data.get("product")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")

        # check the product is exist in previous order
        if not Order.objects.filter(
            payment_status="settlement", order_items__product_id=product.pk
        ).exists():
            raise serializers.ValidationError("Please buy this product first")

        # check if product is already rated
        if Rating.objects.filter(product=product.pk, user=request.user).exists():
            raise serializers.ValidationError("Product is already rated")

        # create rating
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        "product": ["exact"],
    }
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        # get product
        product_id = request.data.get("product")
        product = Product.objects.get(id=product_id)

        # check if product is already in wishlist
        if Wishlist.objects.filter(product=product, user=request.user).exists():
            raise serializers.ValidationError("Product is already in wishlist")

        # create wishlist
        serializer = WishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["product__name"]
    filterset_fields = {
        "product": ["exact"],
        "created_at": ["exact", "gte", "lte"],
    }
    ordering_fields = ["product__name", "created_at"]
    ordering = ["-created_at"]


class TopBrandsAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # get top 5 brands based on total sales and payment status
        top_brands = (
            OrderItem.objects.filter(order__payment_status="settlement")
            .annotate(
                brand_id=F("product__brand"),
                brand_name=F("product__brand__name"),
                brand_logo=F("product__brand__logo"),
                brand_cover=F("product__brand__cover"),
                brand_origin=F("product__brand__origin"),
            )
            .values(
                "brand_id", "brand_name", "brand_cover", "brand_logo", "brand_origin"
            )
            .annotate(total_sales=Sum("quantity"))
            .order_by("-total_sales")[:5]
        )

        # Convert QuerySet to list of dictionaries
        top_brands_list = list(
            top_brands.values(
                "brand_id",
                "brand_name",
                "total_sales",
                "brand_cover",
                "brand_logo",
                "brand_origin",
            )
        )

        return Response(top_brands_list)


class TopCategoryAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # get top 5 brands based on total sales and payment status
        top_category = (
            OrderItem.objects.filter(order__payment_status="settlement")
            .annotate(
                category_id=F("product__category"),
                category_name=F("product__category__name"),
                category_cover=F("product__category__cover"),
            )
            .values("category_id", "category_name", "category_cover")
            .annotate(total_sales=Sum("quantity"))
            .order_by("-total_sales")[:5]
        )

        # Convert QuerySet to list of dictionaries
        top_category_list = list(
            top_category.values(
                "category_id",
                "category_name",
                "total_sales",
                "category_cover",
            )
        )

        return Response(top_category_list)
