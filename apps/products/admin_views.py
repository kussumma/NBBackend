from .models import Wishlist
from django.shortcuts import redirect
from django.contrib import messages


def delete_wishlist_by_product(request, product_id):
    try:
        Wishlist.objects.filter(product__id=product_id).delete()
        messages.success(request, "Wishlist deleted successfully.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("admin:products_wishlist_changelist")
