from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import UserDetails
from apps.cart.models import Cart

User = get_user_model()

# Create user details when user is created
@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)

# Update user last updated when user details is updated
@receiver(post_save, sender=UserDetails)
def update_user_last_updated(sender, instance, **kwargs):
    user = instance.user
    user.last_updated = timezone.now()
    user.save()

# Create cart when user is created
@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)