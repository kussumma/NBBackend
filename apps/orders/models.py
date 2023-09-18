from django.db import models
from django.contrib.auth import get_user_model
import uuid
import secrets
from datetime import date

User = get_user_model()

from apps.products.models import Product, Stock
from apps.coupons.models import Coupon
from apps.shipping.models import Shipping, ShippingRoute


STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('delivered', 'Delivered'),
    ('canceled', 'Canceled'),
    ('returned', 'Returned'),
    ('refunded', 'Refunded'),
    ('completed', 'Completed'),
)

PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
)

RETURN_REFUND_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('rejected', 'Rejected'),
)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupon_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='pending')
    payment_status = models.TextField(choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_ref_code = models.CharField(max_length=100, null=True, blank=True)
    tax_amount = models.PositiveIntegerField(default=0)
    subtotal_amount = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    total_weight = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} - {self.ref_code}'
    
    def generate_ref_code(self):
        # Get the current year, month, and day
        today = date.today()
        year = today.year
        month = today.month
        day = today.day
        
        # Generate a random 8 random as a secret
        secret_number = secrets.token_hex(4).upper()
        
        # Create the order reference code by combining the date and secret number
        refcode = f"{year}{month:02d}{day:02d}{secret_number}"
        
        return refcode
    
    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = self.generate_ref_code().upper()
        super().save(*args, **kwargs)

class ShippingOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_order')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)
    destination = models.ForeignKey(ShippingRoute, on_delete=models.CASCADE, related_name='destination_shippings_orders')
    shipping_type = models.TextField(max_length=100, blank=True, null=True)
    shipping_cost = models.PositiveIntegerField(default=0)
    shipping_ref_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.ref_code} - {self.destination.route}"
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_return_orders')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_order')
    order_item = models.ManyToManyField(OrderItem, related_name='return_order_items')
    detail = models.TextField()
    request_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=RETURN_REFUND_STATUS_CHOICES, default='pending')
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
    status = models.TextField(choices=RETURN_REFUND_STATUS_CHOICES, default='pending')
    result_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.refund_order.user.email} - {self.refund_order.order.ref_code} - {self.created_at}'
