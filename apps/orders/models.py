from django.db import models
from django.contrib.auth import get_user_model
import uuid
import secrets

User = get_user_model()

from apps.products.models import Product, Stock
from apps.coupons.models import Coupon


STATUS_CHOICES = (
    (0, 'Pending'),
    (1, 'Confirmed'),
    (2, 'Shipped'),
    (3, 'Delivered'),
    (4, 'Canceled'),
    (5, 'Returned'),
    (6, 'Refunded'),
    (7, 'Completed'),
)

RETURN_REFUND_STATUS_CHOICES = (
    (0, 'Pending'),
    (1, 'Confirmed'),
    (2, 'Rejected'),
)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', editable=False)
    final_price = models.PositiveIntegerField(default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupon_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

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
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.order.user.email} - {self.product.slug} - {self.quantity}'
    
    def save(self, *args, **kwargs):
        self.total_price = self.stock.price * self.quantity
        super().save(*args, **kwargs)

class ReturnOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_return_orders', editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_order')
    order_item = models.ManyToManyField(OrderItem, related_name='return_order_items')
    detail = models.TextField()
    request_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=RETURN_REFUND_STATUS_CHOICES, default=0)
    result_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.order.user.email} - {self.order.ref_code} - {self.created_at}'
    
class ReturnImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_order = models.ForeignKey(ReturnOrder, on_delete=models.CASCADE, related_name='return_images')
    image = models.ImageField(upload_to='return_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.return_order.user.email} - {self.return_order.order.ref_code} - {self.created_at}'
    
class RefundOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_order = models.OneToOneField(ReturnOrder, on_delete=models.CASCADE, related_name='refund_order')
    refund_amount = models.PositiveIntegerField(default=0)
    refund_receipt = models.ImageField(upload_to='refund_receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=RETURN_REFUND_STATUS_CHOICES, default=0)
    result_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.refund_order.user.email} - {self.refund_order.order.ref_code} - {self.created_at}'
