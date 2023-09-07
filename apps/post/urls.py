from django.urls import path

from apps.post import views

urlpatterns = [
    path("", views.home_page, name='home'),
    path("post/<int:id>", views.post_page, name="post-detail")
]