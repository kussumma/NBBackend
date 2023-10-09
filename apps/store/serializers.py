from rest_framework import serializers
from tools.fileupload_helper import validate_uploaded_file

from .models import Store, Contact, About, Partner, Policy, FAQ, CopyRight


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

    def validate_logo(self, value):
        if value:
            validate_uploaded_file(value, "image")
            return value


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
            validate_uploaded_file(value, "image")
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
