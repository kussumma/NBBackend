from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Favorite, Complaint, ComplaintImage, ProductRequest, FeatureRequest, BugReport, BugReportImage

User = get_user_model()

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['user']

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = '__all__'

class ProductRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRequest
        fields = '__all__'
        read_only_fields = ['user']

class FeatureRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureRequest
        fields = '__all__'
        read_only_fields = ['user']

class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = '__all__'
        read_only_fields = ['user']

class BugReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReportImage
        fields = '__all__'