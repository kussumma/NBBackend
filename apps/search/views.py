from django.db import models
from rest_framework import views, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Search
from .serializers import SearchSerializer
from apps.products.models import Product, Category, Subcategory, Subsubcategory, Brand
from apps.store.models import FAQ
from apps.products.serializers import ProductSerializer, CategorySerializer, SubcategorySerializer, SubsubcategorySerializer, BrandSerializer
from apps.store.serializers import FAQSerializer

User = get_user_model()

class SearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search_query = request.query_params.get('q', '')
        search_terms = search_query.split()

        product_results = Product.objects.none()
        category_results = Category.objects.none()
        subcategory_results = Subcategory.objects.none()
        subsubcategory_results = Subsubcategory.objects.none()
        brand_results = Brand.objects.none()
        faq_results = FAQ.objects.none()

        # perform search
        for term in search_terms:
            product_results |= Product.objects.filter(
                models.Q(name__icontains=term) | 
                models.Q(description__icontains=term ) |
                models.Q(category__name__icontains=term) |
                models.Q(subcategory__name__icontains=term) |
                models.Q(subsubcategory__name__icontains=term) |
                models.Q(brand__name__icontains=term)
            )

            category_results |= Category.objects.filter(name__icontains=term)
            subcategory_results |= Subcategory.objects.filter(name__icontains=term)
            subsubcategory_results |= Subsubcategory.objects.filter(name__icontains=term)
            brand_results |= Brand.objects.filter(models.Q(name__icontains=term) | models.Q(origin__icontains=term))
            faq_results |= FAQ.objects.filter(models.Q(question__icontains=term) | models.Q(answer__icontains=term))

        # Serialize the search results
        product_serializer = ProductSerializer(product_results, many=True)
        category_serializer = CategorySerializer(category_results, many=True)
        subcategory_serializer = SubcategorySerializer(subcategory_results, many=True)
        subsubcategory_serializer = SubsubcategorySerializer(subsubcategory_results, many=True)
        brand_serializer = BrandSerializer(brand_results, many=True)
        faq_serializer = FAQSerializer(faq_results, many=True)

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
            'search': search_serializer.data
        })

