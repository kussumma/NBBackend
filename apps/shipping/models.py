from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ShippingType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ShippingRoute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    route = models.CharField(max_length=100, blank=True, null=True)
    is_city = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.route}"
    
class ShippingRoutePerType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.CASCADE, related_name='type_routes')
    origin_code = models.CharField(max_length=5, blank=True, null=True)
    origin_city = models.CharField(max_length=100, blank=True, null=True)
    destination_code = models.CharField(max_length=5, blank=True, null=True)
    destination_city = models.CharField(max_length=100, blank=True, null=True)
    published_rate = models.PositiveIntegerField(default=0)
    discount_rate = models.PositiveIntegerField(default=0)
    shipping_duration = models.CharField(max_length=100, blank=True, null=True)
    lead_time = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shipping_type} - {self.origin_city} - {self.destination_city}"
    
class ShippingCommodity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Shipping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shippings')
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_phone = models.CharField(max_length=100, blank=True, null=True)
    receiver_address = models.CharField(max_length=100, blank=True, null=True)
    origin = models.ForeignKey(ShippingRoute, on_delete=models.CASCADE, related_name='origin_shippings')
    destination = models.ForeignKey(ShippingRoute, on_delete=models.CASCADE, related_name='destination_shippings')
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.CASCADE, related_name='type_shippings')
    shipping_commodity = models.ForeignKey(ShippingCommodity, on_delete=models.CASCADE, related_name='commodity_shippings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - "
