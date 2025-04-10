from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.accounts.views import GoogleLogin
from tools.file_server import FileAPIView

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    path("", include("apps.orders.admin_urls")),
    path("", include("apps.products.admin_urls")),
    # Basic Auth
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    # Search
    path("api/", include("apps.search.urls")),
    # Account
    path("api/", include("apps.accounts.urls")),
    # Products
    path("api/", include("apps.products.urls")),
    # Cart
    path("api/", include("apps.cart.urls")),
    # Coupons
    path("api/", include("apps.coupons.urls")),
    # Orders
    path("api/", include("apps.orders.urls")),
    # Customers
    path("api/", include("apps.customers.urls")),
    # Store
    path("api/", include("apps.store.urls")),
    # Blogs
    path("api/", include("apps.blogs.urls")),
    # Shipping
    path("api/", include("apps.shipping.urls")),
    # Payments
    path("api/", include("apps.payments.urls")),
    # File Server
    path("media/<str:collection>/<str:filename>", FileAPIView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
