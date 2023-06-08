from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StoreViewSet, ContactViewSet, AboutViewSet, PartnerViewSet, PolicyViewSet, FAQViewSet, CopyRightViewSet
)

router = DefaultRouter()
router.register('store', StoreViewSet)
router.register('contact', ContactViewSet)
router.register('about', AboutViewSet)
router.register('partner', PartnerViewSet)
router.register('policy', PolicyViewSet)
router.register('faq', FAQViewSet)
router.register('copy_right', CopyRightViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]