from django.urls import path

from apps.post import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("post/<int:post_id>", views.PostPageView.as_view(), name="post-detail"),
    path("post/new_post", views.NewPostView.as_view(), name="new-post")
]