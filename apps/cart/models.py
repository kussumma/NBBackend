from django.db import models
from django.contrib.auth import get_user_model
import uuid

from apps.products.models import Product, Stock

User = get_user_model()


class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s cart"


class CartItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_products"
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="cart_stocks"
    )
    quantity = models.PositiveIntegerField(default=1, db_index=True)
    total_price = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_selected = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.cart.user.email} - {self.product.slug} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.product = self.stock.product
        self.total_price = (
            self.stock.price * self.quantity * (1 - self.stock.discount / 100)
        )
        super().save(*args, **kwargs)

    def increase_quantity(self, quantity=1):
        self.quantity += quantity
        self.save()

    def decrease_quantity(self, quantity=1):
        if self.quantity > quantity:
            self.quantity -= quantity
        else:
            self.quantity = 1
        self.save()

    def set_as_selected(self, selected):
        if selected:
            self.is_selected = True
        else:
            self.is_selected = False
        self.save()
