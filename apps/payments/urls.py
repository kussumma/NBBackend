from django.urls import path

from .views import PaymentAPIViews, PaymentStatusAPIViews, PaymentNotificationAPIView

urlpatterns = [
    path("v1/payment/", PaymentAPIViews.as_view(), name="payment"),
    path("v1/payment-status/", PaymentStatusAPIViews.as_view(), name="payment-status"),
    path(
        "v1/payment-notification/e2e584040e0aa50cac05b41c30898b5ce426e5ef5a453f4550ec39606c0f210358b6568da04672407997fb449cf010346/",
        PaymentNotificationAPIView.as_view(),
        name="payment-notification",
    ),
]
