from django.db import models
from django.contrib.auth import get_user_model
import uuid
import secrets

User = get_user_model()

from apps.products.models import Product, Stock
from apps.coupons.models import Coupon


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    final_price = models.PositiveIntegerField(default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupon_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'
    
    def generate_ref_code(self):
        return secrets.token_urlsafe(12)
    
    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = self.generate_ref_code().upper()
        super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='order_stocks')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.order.user.email} - {self.product.slug} - {self.quantity}'
    
    def save(self, *args, **kwargs):
        self.price = self.stock.price * self.quantity
        super().save(*args, **kwargs)
