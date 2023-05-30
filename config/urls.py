
from django.contrib import admin
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # Auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/jwt/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/', include('djoser.social.urls')),

    # Account
    path('api/', include('apps.accounts.urls')),

    # Products
    path('api/', include('apps.products.urls')),

    # Cart
    path('api/', include('apps.cart.urls')),

]

if settings.DEBUG:
    urlpatterns += path('admin/', admin.site.urls),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

