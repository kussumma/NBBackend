from django.db import models
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import time
from django.utils import timezone
import datetime
from django.db.models import Q

from .models import Search
from .serializers import SearchSerializer
from apps.products.models import Product, Brand
from apps.store.models import FAQ
from apps.blogs.models import Blog
from apps.coupons.models import Coupon
from apps.products.serializers import (
    ProductSerializer,
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
        # start timer
        start_time = time.time()

        # get search query
        search_query = request.query_params.get("q", "")

        if not search_query:
            return Response({})

        # split search query into individual search terms
        search_terms = search_query.split()

        # Initialize Q objects
        product_query = Q()
        brand_query = Q()
        faq_query = Q()
        blog_query = Q()
        coupon_query = Q()

        # Build Q objects
        for term in search_terms:
            product_query |= (
                Q(name__icontains=term)
                | Q(description__icontains=term)
                | Q(category__name__icontains=term)
                | Q(subcategory__name__icontains=term)
                | Q(subsubcategory__name__icontains=term)
                | Q(product_stock__sku__icontains=term)
                | Q(product_stock__discount__icontains=term)
                | Q(product_stock__price__icontains=term)
                | Q(product_stock__size__icontains=term)
                | Q(product_stock__color__icontains=term)
                | Q(product_stock__variant__icontains=term)
            )
            brand_query |= Q(name__icontains=term) | Q(origin__icontains=term)
            faq_query |= Q(question__icontains=term) | Q(answer__icontains=term)
            blog_query |= Q(title__icontains=term) | Q(content__icontains=term)
            coupon_query |= (
                Q(prefix_code__icontains=term)
                | Q(name__icontains=term)
                | Q(discount_value__icontains=term)
            )

        # Perform search
        product_results = Product.objects.filter(
            product_query, is_active=True
        ).order_by("name")[:10]
        brand_results = Brand.objects.filter(brand_query).order_by("name")[:5]
        faq_results = FAQ.objects.filter(faq_query).order_by("question")[:5]
        blog_results = Blog.objects.filter(blog_query, is_published=True).order_by(
            "title"
        )[:5]
        coupon_results = Coupon.objects.filter(
            coupon_query, is_active=True, is_private=False
        ).order_by("name")[:5]

        # Serialize the search results
        product_serializer = ProductSerializer(product_results, many=True)
        brand_serializer = BrandSerializer(brand_results, many=True)
        faq_serializer = FAQSerializer(faq_results, many=True)
        blog_serializer = BlogSerializer(blog_results, many=True)
        coupon_serializer = CouponSerializer(coupon_results, many=True)

        # end timer
        end_time = time.time()

        # calculate time taken
        time_taken = end_time - start_time
        time_taken = f"{round(time_taken, 3)} seconds"

        return Response(
            {
                "products": product_serializer.data,
                "brands": brand_serializer.data,
                "faqs": faq_serializer.data,
                "blogs": blog_serializer.data,
                "coupons": coupon_serializer.data,
                "time_taken": time_taken,
            }
        )


class StoreSearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search_query = request.query_params.get("q", "")
        contains_profane = []

        if search_query and len(search_query) > 3:
            # Create a new search record
            try:
                profanity_filter = AdvancedProfanityFilter()

                # store search if its profane
                for term in search_query.split():
                    if profanity_filter.is_profanity(term):
                        contains_profane.append(term)

                if len(contains_profane) < 1:
                    user = request.user if request.user.is_authenticated else None
                    Search.objects.create(query=search_query, user=user)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"search_query": search_query}, status=status.HTTP_200_OK)


class TrendingSearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Get the current date and time
        now = timezone.now()

        # Calculate the date and time one week ago
        one_week_ago = now - datetime.timedelta(weeks=1)

        # Modify the query to filter the searches that were made after the date and time calculated above
        trending_searches = (
            Search.objects.filter(
                created_at__gte=one_week_ago
            )  # assuming `created_at` is the field that stores when the search was made
            .values("query")
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
