from django.urls import path, include

from .views import ( PaymentAPIViews, payment_testing )

urlpatterns = [
    path('v1/payment/', PaymentAPIViews.as_view(), name='payment'),
    path('v1/payment-testing/', payment_testing, name='payment-testing'),
]