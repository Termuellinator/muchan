from django.urls import path

from apps.user import views

urlpatterns = [
    path("user/profile/", views.UserProfileView.as_view(), name="profile"),
    path("user/logout/", views.UserLogoutView.as_view(), name="logout"),
]