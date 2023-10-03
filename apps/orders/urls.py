from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrderViewset,
    ReturnOrderViewset,
    RefundOrderViewset,
    ConfirmOrderAPIView,
    BookShipmentAPIView,
)

router = DefaultRouter()
router.register("order", OrderViewset, basename="order")
router.register("return-order", ReturnOrderViewset, basename="return-order")
router.register("refund-order", RefundOrderViewset, basename="refund-order")

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/confirm-order/<uuid:pk>/",
        ConfirmOrderAPIView.as_view(),
        name="confirm_order",
    ),
    path(
        "v1/book-shipment/<uuid:pk>/",
        BookShipmentAPIView.as_view(),
        name="book_shipment",
    ),
]
