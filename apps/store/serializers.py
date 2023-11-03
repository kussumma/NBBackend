from rest_framework import serializers
from tools.fileupload_helper import FileUploadHelper

from .models import Contact, About, Partner, Investor, Policy, FAQ, CopyRight


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"

    def validate_logo(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = "__all__"

    def validate_logo(self, value):
        if value:
            value = FileUploadHelper(value, webp=True).validate()
            return value


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class CopyRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyRight
        fields = "__all__"
