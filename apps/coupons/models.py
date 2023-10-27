import secrets
import uuid
from django import db
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from django.conf import settings
import hashlib
import base64
from tools.filestorage_helper import GridFSStorage

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
    code = models.CharField(max_length=250, unique=True, editable=False)
    prefix_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250, unique=True)
    cover = models.ImageField(
        storage=GridFSStorage(collection="coupon_covers"), default="default.jpg"
    )
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    discount_value = models.PositiveBigIntegerField(default=0)
    min_purchase = models.PositiveBigIntegerField(default=0)
    max_purchase = models.PositiveBigIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.prefix_code}{self.decode_coupon_code(self.code)}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if self.prefix_code.upper() == "RANDOM" or len(self.prefix_code) < 8:
            self.prefix_code = self.generate_prefix_code()
        else:
            self.prefix_code = self.prefix_code.upper()[:8]
        super().save(*args, **kwargs)

    def generate_code(self):
        code = secrets.token_urlsafe(12).upper()[:8]
        return fernet.encrypt(code.encode()).decode()

    def generate_prefix_code(self):
        prefix = secrets.token_urlsafe(12).upper()[:8]
        return prefix

    def is_verified(self, code):
        try:
            code = code.encode()
            decrypted_code = fernet.decrypt(self.code.encode())
            return code == decrypted_code
        except InvalidToken:
            return False

    def decode_coupon_code(self, code):
        try:
            code = code.encode()
            return fernet.decrypt(code).decode()
        except InvalidToken:
            return "Invalid code"

    def is_valid(self):
        try:
            now = timezone.now()
            return self.is_active and self.valid_from <= now and self.valid_to >= now
        except Exception:
            return False


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
