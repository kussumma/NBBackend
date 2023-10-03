from django.urls import path

from .views import PaymentAPIViews, PaymentStatusAPIViews

urlpatterns = [
    path("v1/payment/", PaymentAPIViews.as_view(), name="payment"),
    path("v1/payment-status/", PaymentStatusAPIViews.as_view(), name="payment-status"),
]
