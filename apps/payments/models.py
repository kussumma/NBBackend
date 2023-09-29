from django.db import models
from django.contrib.auth import get_user_model
import uuid

from apps.orders.models import Order

User = get_user_model()

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    token = models.CharField(max_length=100)
    redirect_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.created_at} - {self.user.email} - {self.order.ref_code}'
