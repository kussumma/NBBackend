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
from apps.products.serializers import ProductSerializer, SearchCategorySerializer, SearchSubcategorySerializer, SubsubcategorySerializer, BrandSerializer
from apps.store.serializers import FAQSerializer
from apps.blogs.serializers import BlogSerializer
from apps.coupons.serializers import CouponSerializer

User = get_user_model()

class SearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):

        # get search query
        search_query = request.query_params.get('q', '')
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
                models.Q(name__icontains=term) | 
                models.Q(description__icontains=term ) |
                models.Q(category__name__icontains=term) |
                models.Q(subcategory__name__icontains=term) |
                models.Q(subsubcategory__name__icontains=term) |
                models.Q(brand__name__icontains=term) |
                models.Q(brand__origin__icontains=term)
            )

            category_results |= Category.objects.filter(name__icontains=term)
            subcategory_results |= Subcategory.objects.filter(name__icontains=term)
            subsubcategory_results |= Subsubcategory.objects.filter(name__icontains=term)
            brand_results |= Brand.objects.filter(models.Q(name__icontains=term) | models.Q(origin__icontains=term))
            faq_results |= FAQ.objects.filter(models.Q(question__icontains=term) | models.Q(answer__icontains=term))
            blog_results |= Blog.objects.filter(models.Q(title__icontains=term) | models.Q(description__icontains=term))
            coupon_results |= Coupon.objects.filter(models.Q(code__icontains=term) | models.Q(name__icontains=term))

        # Serialize the search results
        product_serializer = ProductSerializer(product_results, many=True)
        category_serializer = SearchCategorySerializer(category_results, many=True)
        subcategory_serializer = SearchSubcategorySerializer(subcategory_results, many=True)
        subsubcategory_serializer = SubsubcategorySerializer(subsubcategory_results, many=True)
        brand_serializer = BrandSerializer(brand_results, many=True)
        faq_serializer = FAQSerializer(faq_results, many=True)
        blog_serializer = BlogSerializer(blog_results, many=True)
        coupon_serializer = CouponSerializer(coupon_results, many=True)

        # Create a new search record
        user = request.user if request.user.is_authenticated else None
        search = Search.objects.create(
            query=search_query,
            user=user
        )

        search_serializer = SearchSerializer(search)

        return Response({
            'products': product_serializer.data,
            'categories': category_serializer.data,
            'subcategories': subcategory_serializer.data,
            'subsubcategories': subsubcategory_serializer.data,
            'brands': brand_serializer.data,
            'faqs': faq_serializer.data,
            'blogs': blog_serializer.data,
            'coupons': coupon_serializer.data,
            'search': search_serializer.data
        })
    

class TrendingSearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # get trending searches
        trending_searches = Search.objects.values('query').annotate(search_count=models.Count('query')).order_by('-search_count')[:10]

       # Manually extract the 'search_count' from the annotated query result
        trending_searches_with_count = []
        for entry in trending_searches:
            search_query = entry['query']
            search_count = entry['search_count']
            trending_searches_with_count.append({'query': search_query, 'search_count': search_count})

        return Response({
            'trending_searches': trending_searches_with_count
        })
