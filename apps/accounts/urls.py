from django.urls import include, path

from .views import UserDetailsView, UserListView, StaffListView

urlpatterns = [
    path('account/<uuid:id>/', UserDetailsView.as_view(), name='user-details'),
    path('account/list/', UserListView.as_view(), name='user-list'),
    path('account/staff/', StaffListView.as_view(), name='staff-list'),
]