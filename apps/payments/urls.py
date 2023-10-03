from django.urls import path

from .views import PaymentAPIViews, FinishPaymentAPIViews, payment_testing

urlpatterns = [
    path("v1/payment/", PaymentAPIViews.as_view(), name="payment"),
    path("v1/finish-payment/", FinishPaymentAPIViews.as_view(), name="finish-payment"),
]
