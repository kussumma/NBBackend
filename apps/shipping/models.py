from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

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
    
class ShippingGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class ShippingType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.name

class ShippingGroupItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping_group = models.ForeignKey(ShippingGroup, on_delete=models.CASCADE, related_name='shipping_group_items')
    shipping_route = models.ForeignKey(ShippingRoute, on_delete=models.CASCADE, related_name='shipping_route_items')

    def __str__(self):
        return f"{self.shipping_group.name} - {self.shipping_route.name}"

class ShippingGroupTariff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping_group = models.ForeignKey(ShippingGroup, on_delete=models.CASCADE, related_name='shipping_group_tariffs')
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.CASCADE, related_name='shipping_type_tariffs')
    tariff  = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shipping_group.name} - {self.shipping_type.name}"

class Shipping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shippings')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)
    destination = models.ForeignKey(ShippingRoute, on_delete=models.CASCADE, related_name='destination_shippings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.destination.route}"
