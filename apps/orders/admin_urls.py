from django.urls import path

from .admin_views import confirm_order_view, book_shipment_view

urlpatterns = [
    path("confirm-order/<uuid:pk>/", confirm_order_view, name="confirm-order"),
    path("book-shipment/<uuid:pk>/", book_shipment_view, name="book-shipment"),
]
