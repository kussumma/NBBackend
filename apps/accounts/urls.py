from django.urls import path

from .views import UserListView, StaffListView, SubscribeNewsletterView

urlpatterns = [
    path("v1/account/list/", UserListView.as_view(), name="user-list"),
    path("v1/account/staff/", StaffListView.as_view(), name="staff-list"),
    path(
        "v1/newsletter/subscribe/", SubscribeNewsletterView.as_view(), name="subscribe"
    ),
]
