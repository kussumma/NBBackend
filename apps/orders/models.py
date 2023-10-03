from django.db import models
from django.contrib.auth import get_user_model
import uuid
import secrets

User = get_user_model()

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("shipping", "Shipping"),
    ("returned", "Returned"),
    ("refunded", "Refunded"),
    ("complete", "Complete"),
)

PAYMENT_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("capture", "Capture"),
    ("settlement", "Settlement"),
    ("cancel", "Cancel"),
    ("expired", "Expired"),
)

RETURN_REFUND_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("rejected", "Rejected"),
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    coupon = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default="pending")
    payment_status = models.TextField(choices=PAYMENT_STATUS_CHOICES, default="pending")
    payment_ref_code = models.UUIDField(null=True, blank=True)
    tax_amount = models.PositiveIntegerField(default=0)
    shipping_amount = models.PositiveIntegerField(default=0)
    subtotal_amount = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    total_weight = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.created_at} - {self.user.email} - {self.ref_code}"

    def generate_ref_code(self):
        # Generate a random 16-digit hex number
        secret_number = secrets.token_hex(8)

        # Create the order reference code by secret number
        refcode = secret_number.upper()

        return refcode

    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = self.generate_ref_code()
        super().save(*args, **kwargs)


class OrderShipping(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="order_shipping"
    )
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=250)
    destination_route = models.CharField(max_length=250)
    shipping_type = models.TextField(max_length=100, blank=True, null=True)
    shipping_type_name = models.TextField(max_length=100, blank=True, null=True)
    shipping_ref_code = models.CharField(max_length=100, null=True, blank=True)
    shipping_estimation = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.ref_code} - {self.destination_route}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField(default=1)
    product_name = models.CharField(max_length=250)
    product_discount = models.IntegerField(default=0)
    stock_price = models.IntegerField(default=0)
    stock_image = models.CharField(max_length=250, null=True, blank=True)
    stock_size = models.CharField(max_length=100, null=True, blank=True)
    stock_color = models.CharField(max_length=100, null=True, blank=True)
    stock_other = models.CharField(max_length=100, null=True, blank=True)
    stock_weight = models.IntegerField(default=0)
    stock_length = models.IntegerField(default=0)
    stock_width = models.IntegerField(default=0)
    stock_height = models.IntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.order.ref_code} - {self.product_name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = self.stock_price * self.quantity
        super().save(*args, **kwargs)


class ReturnOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_return_orders"
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="return_order"
    )
    order_item = models.ManyToManyField(OrderItem, related_name="return_order_items")
    detail = models.TextField()
    request_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=RETURN_REFUND_STATUS_CHOICES, default="pending")
    result_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.order.user.email} - {self.order.ref_code} - {self.created_at}"


class ReturnImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_order = models.ForeignKey(
        ReturnOrder, on_delete=models.CASCADE, related_name="return_images"
    )
    image = models.ImageField(upload_to="return_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.return_order.user.email} - {self.return_order.order.ref_code} - {self.created_at}"


class RefundOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_order = models.OneToOneField(
        ReturnOrder, on_delete=models.CASCADE, related_name="refund_order"
    )
    refund_amount = models.PositiveIntegerField(default=0)
    refund_receipt = models.ImageField(
        upload_to="refund_receipts/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=RETURN_REFUND_STATUS_CHOICES, default="pending")
    result_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.refund_order.user.email} - {self.refund_order.order.ref_code} - {self.created_at}"
