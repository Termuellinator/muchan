from django.urls import path
from rest_framework import routers

from apps.post import views, api_views


router = routers.SimpleRouter()
router.register("api/v1/post", api_views.PostViewSet)
router.register("api/v1/category", api_views.CategoryViewSet)
router.register("api/v1/tag", api_views.TagViewSet)
router.register("api/v1/comment", api_views.CommentViewSet)


urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("post/<int:post_id>", views.PostPageView.as_view(), name="post-detail"),
    path("post/new_post", views.NewPostView.as_view(), name="new-post"),
    path("post/upvote/<int:post_id>", views.UpVotePostView.as_view(),
         name="post-upvote"),
    path("post/downvote/<int:post_id>", views.DownVotePostView.as_view(),
         name="post-downvote"),
    path("comment/upvote/<int:comment_id>", views.UpVoteCommentView.as_view(),
         name="comment-upvote"),
    path("comment/downvote/<int:comment_id>", views.DownVoteCommentView.as_view(),
         name="comment-downvote"),
    *router.urls,
]