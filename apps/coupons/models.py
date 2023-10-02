import secrets
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
import base64

User = get_user_model()

# Generate a 32-byte hash of the Django secret key
hash = hashlib.sha256(settings.SECRET_KEY.encode()).digest()

# Encode the hash as a URL-safe base64-encoded string
key = base64.urlsafe_b64encode(hash)

fernet = Fernet(key)


class DiscountType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.BinaryField(max_length=250, unique=True, editable=False)
    name = models.CharField(max_length=100)
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    discount_value = models.PositiveBigIntegerField(default=0)
    min_purchase = models.PositiveBigIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        code = secrets.token_urlsafe(8).upper()
        return fernet.encrypt(code.encode())

    def decode_coupon_code(self, code):
        return fernet.decrypt(code)

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now and self.valid_to >= now


class CouponUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_coupons"
    )
    is_used = models.BooleanField(default=True)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coupon.name} - {self.user}"


class CouponBanner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="coupon_banners"
    )
    image = models.ImageField(upload_to="coupon_banners")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.coupon.name} - {self.image.url}"
