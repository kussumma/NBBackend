from django.urls import path

from .admin_views import delete_wishlist_by_product

urlpatterns = [
    path(
        "delete-wishlist-by-product/<uuid:product_id>/",
        delete_wishlist_by_product,
        name="delete-wishlist-by-product",
    ),
]
