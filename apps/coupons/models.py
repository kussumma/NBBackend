import secrets
import hashlib
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class DiscountType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, editable=False)
    hashed_code = models.CharField(max_length=64, unique=True, editable=False)
    name = models.CharField(max_length=100)
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    discount_value = models.PositiveBigIntegerField(default=0)
    min_purchase = models.PositiveBigIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code().upper()
            self.hashed_code = self.hash_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        return secrets.token_urlsafe(8)

    def hash_code(self):
        sha256 = hashlib.sha256()
        sha256.update(self.code.encode('utf-8'))
        return sha256.hexdigest()

    def verify_code(self, code):
        hashed_input = hashlib.sha256(code.encode('utf-8')).hexdigest()
        return self.hashed_code == hashed_input

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now and self.valid_to >= now

class CouponUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_coupons', editable=False)
    is_used = models.BooleanField(default=True)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.coupon.name} - {self.user}'
    
class Promo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PromoBanner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='promo_banners')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.promo.name} - {self.id}'

