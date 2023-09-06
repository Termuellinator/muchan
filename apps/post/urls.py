from django.urls import path

from apps.post import views

urlpatterns = [
    path("", views.home_page, name='home'),
   # path("resource/<int:id>", views.resource_detail, name="resource-detail")
]