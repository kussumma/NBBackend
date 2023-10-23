from django.db import models
from rest_framework import views, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Search
from .serializers import SearchSerializer
from apps.products.models import Product, Category, Subcategory, Subsubcategory, Brand
from apps.store.models import FAQ
from apps.blogs.models import Blog
from apps.coupons.models import Coupon
from apps.products.serializers import (
    ProductSerializer,
    SearchCategorySerializer,
    SearchSubcategorySerializer,
    SubsubcategorySerializer,
    BrandSerializer,
)
from apps.store.serializers import FAQSerializer
from apps.blogs.serializers import BlogSerializer
from apps.coupons.serializers import CouponSerializer
from tools.profanity_helper import AdvancedProfanityFilter

User = get_user_model()


class SearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # get search query
        search_query = request.query_params.get("q", "")

        if search_query:
            # split search query into individual search terms
            search_terms = search_query.split()

            # initialize empty querysets
            product_results = Product.objects.none()
            category_results = Category.objects.none()
            subcategory_results = Subcategory.objects.none()
            subsubcategory_results = Subsubcategory.objects.none()
            brand_results = Brand.objects.none()
            faq_results = FAQ.objects.none()
            blog_results = Blog.objects.none()
            coupon_results = Coupon.objects.none()

            # perform search
            for term in search_terms:
                product_results |= Product.objects.filter(
                    models.Q(name__icontains=term)
                    | models.Q(description__icontains=term)
                    | models.Q(product_stock__sku__icontains=term)
                    | models.Q(product_stock__discount__icontains=term)
                    | models.Q(product_stock__price__icontains=term)
                    | models.Q(product_stock__size__icontains=term)
                    | models.Q(product_stock__color__icontains=term)
                    | models.Q(product_stock__other__icontains=term)
                )[:5]

                category_results |= Category.objects.filter(name__icontains=term)[:5]
                subcategory_results |= Subcategory.objects.filter(name__icontains=term)[
                    :5
                ]
                subsubcategory_results |= Subsubcategory.objects.filter(
                    name__icontains=term
                )[:5]
                brand_results |= Brand.objects.filter(
                    models.Q(name__icontains=term) | models.Q(origin__icontains=term)
                )[:5]
                faq_results |= FAQ.objects.filter(
                    models.Q(question__icontains=term)
                    | models.Q(answer__icontains=term)
                )[:5]
                blog_results |= Blog.objects.filter(
                    models.Q(title__icontains=term) | models.Q(content__icontains=term)
                )[:5]
                coupon_results |= Coupon.objects.filter(
                    models.Q(prefix_code__icontains=term)
                    | models.Q(name__icontains=term)
                    | models.Q(discount_value__icontains=term)
                )[:5]

            # Serialize the search results
            product_serializer = ProductSerializer(product_results, many=True)
            category_serializer = SearchCategorySerializer(category_results, many=True)
            subcategory_serializer = SearchSubcategorySerializer(
                subcategory_results, many=True
            )
            subsubcategory_serializer = SubsubcategorySerializer(
                subsubcategory_results, many=True
            )
            brand_serializer = BrandSerializer(brand_results, many=True)
            faq_serializer = FAQSerializer(faq_results, many=True)
            blog_serializer = BlogSerializer(blog_results, many=True)
            coupon_serializer = CouponSerializer(coupon_results, many=True)

            # Create a new search record
            profanity_filter = AdvancedProfanityFilter()
            search_query = profanity_filter.censor(search_query)

            user = request.user if request.user.is_authenticated else None
            search = Search.objects.create(query=search_query, user=user)

            search_serializer = SearchSerializer(search)

            # get trending searches
            trending_searches = (
                Search.objects.values("query")
                .annotate(search_count=models.Count("query"))
                .order_by("-search_count")[:5]
            )

            serialized_trending_searches = []
            for entry in trending_searches:
                search_query = entry["query"]
                search_count = entry["search_count"]
                serialized_trending_searches.append(
                    {"query": search_query, "search_count": search_count}
                )

            return Response(
                {
                    "trending_searches": serialized_trending_searches,
                    "products": product_serializer.data,
                    "categories": category_serializer.data,
                    "subcategories": subcategory_serializer.data,
                    "subsubcategories": subsubcategory_serializer.data,
                    "brands": brand_serializer.data,
                    "faqs": faq_serializer.data,
                    "blogs": blog_serializer.data,
                    "coupons": coupon_serializer.data,
                    "search": search_serializer.data,
                }
            )
        else:
            return Response({})


class TrendingSearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # get trending searches
        trending_searches = (
            Search.objects.values("query")
            .annotate(search_count=models.Count("query"))
            .order_by("-search_count")[:5]
        )

        # Manually extract the 'search_count' from the annotated query result
        trending_searches_with_count = []
        for entry in trending_searches:
            search_query = entry["query"]
            search_count = entry["search_count"]
            trending_searches_with_count.append(
                {"query": search_query, "search_count": search_count}
            )

        return Response({"trending_searches": trending_searches_with_count})


class SearchHistoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # get search history
        search_history = Search.objects.filter(user=request.user).order_by(
            "-created_at"
        )

        # Serialize the search history
        search_history_serializer = SearchSerializer(search_history, many=True)

        return Response(search_history_serializer.data)
