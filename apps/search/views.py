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

            # Initialize empty lists to collect results
            product_results = set()
            category_results = set()
            subcategory_results = set()
            subsubcategory_results = set()
            brand_results = set()
            faq_results = set()
            blog_results = set()
            coupon_results = set()

            # perform search
            for term in search_terms:
                product_results.update(
                    Product.objects.filter(
                        models.Q(name__icontains=term)
                        | models.Q(description__icontains=term)
                        | models.Q(product_stock__sku__icontains=term)
                        | models.Q(product_stock__discount__icontains=term)
                        | models.Q(product_stock__price__icontains=term)
                        | models.Q(product_stock__size__icontains=term)
                        | models.Q(product_stock__color__icontains=term)
                        | models.Q(product_stock__other__icontains=term)
                    ).order_by("name")
                )

                category_results.update(Category.objects.filter(name__icontains=term))
                subcategory_results.update(
                    Subcategory.objects.filter(name__icontains=term)
                )
                subsubcategory_results.update(
                    Subsubcategory.objects.filter(name__icontains=term)
                )
                brand_results.update(
                    Brand.objects.filter(
                        models.Q(name__icontains=term)
                        | models.Q(origin__icontains=term)
                    )
                )
                faq_results.update(
                    FAQ.objects.filter(
                        models.Q(question__icontains=term)
                        | models.Q(answer__icontains=term)
                    )
                )
                blog_results.update(
                    Blog.objects.filter(
                        models.Q(title__icontains=term)
                        | models.Q(content__icontains=term)
                    )
                )
                coupon_results.update(
                    Coupon.objects.filter(
                        models.Q(prefix_code__icontains=term)
                        | models.Q(name__icontains=term)
                        | models.Q(discount_value__icontains=term)
                    )
                )

            # Limit the results to the top 5 for each category
            product_results = list(product_results)[:5]
            category_results = list(category_results)[:5]
            subcategory_results = list(subcategory_results)[:5]
            subsubcategory_results = list(subsubcategory_results)[:5]
            brand_results = list(brand_results)[:5]
            faq_results = list(faq_results)[:5]
            blog_results = list(blog_results)[:5]
            coupon_results = list(coupon_results)[:5]

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

            return Response(
                {
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
