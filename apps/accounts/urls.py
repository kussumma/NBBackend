from django.urls import include, path

from .views import UserDetailsView

urlpatterns = [
    path('account/<uuid:id>/', UserDetailsView.as_view(), name='user-details'),
]