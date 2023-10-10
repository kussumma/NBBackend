from django.urls import path

from .views import UserListView, StaffListView

urlpatterns = [
    path("account/list/", UserListView.as_view(), name="user-list"),
    path("account/staff/", StaffListView.as_view(), name="staff-list"),
]
