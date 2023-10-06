from django.urls import path
from django.contrib.auth import views as auth_views

from apps.user import views, api_views

api_urlpatterns = [
    path('api/v1/login', api_views.UserLoginView.as_view(), name="login-token"),
]

urlpatterns = [
    path("user/profile/", views.UserProfileView.as_view(), name="profile"),
    path("user/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("user/change_password/", 
         auth_views.PasswordChangeView.as_view(
             template_name="user/change_pw.html"), 
        name="change_password"),
    path("user/register/", views.RegisterUserView.as_view(), name="register"),
    path("user/modify_profile/", views.ModifyUserView.as_view(),
         name="modify_profile"),
    *api_urlpatterns,
]