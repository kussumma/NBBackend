from rest_framework import serializers

from .models import ( Search )

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
        read_only_fields = ['user']