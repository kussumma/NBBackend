from django.db import models
from django.contrib.auth import get_user_model
import uuid

from apps.orders.models import Order

User = get_user_model()

class Shipping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_shipping')
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)
    village = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Indonesia")
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_whatsapp = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    total_weight = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    shipping_cost = models.IntegerField(blank=True, null=True)
    shipping_service = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.city}, {self.province} {self.country}"
        
