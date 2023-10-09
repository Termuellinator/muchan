from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.post import models, serializers, mixins, permissions


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AuthorSuperOrReadOnly,)

    queryset = (
        models.Post.objects
        .select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all())

    serializer_class = serializers.PostModelSerializer


class CategoryViewSet(mixins.DenyDeletionOfDefaultCategoryMixin,
                      viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedCreateOrSuperDeleteOrReadOnly,)
    queryset = (models.Category.objects.all())

    serializer_class = serializers.CategoryModelSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedCreateOrSuperDeleteOrReadOnly,)
    queryset = (models.Tag.objects.all())

    serializer_class = serializers.TagModelSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AuthorSuperOrReadOnly,)
    queryset = (models.Comment.objects.all())

    serializer_class = serializers.CommentModelSerializer


class UpVotePostView(APIView):
    """Upvote a post for an authenticated user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            self.post = models.Post.objects.get(pk=post_id)
            self.post.userUpVotes.add(request.user)
            self.post.userDownVotes.remove(request.user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND)


class DownVotePostView(APIView):
    """Downvote a post for an authenticated user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            self.post = models.Post.objects.get(pk=post_id)
            self.post.userDownVotes.add(request.user)
            self.post.userUpVotes.remove(request.user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND)


class UpVoteCommentView(APIView):
    """Upvote a comment for an authenticated user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, comment_id):
        try:
            self.comment = models.Comment.objects.get(pk=comment_id)
            self.comment.userUpVotes.add(request.user)
            self.comment.userDownVotes.remove(request.user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND)


class DownVoteCommentView(APIView):
    """Downvote a comment for an authenticated user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, comment_id):
        try:
            self.comment = models.Comment.objects.get(pk=comment_id)
            self.comment.userDownVotes.add(request.user)
            self.comment.userUpVotes.remove(request.user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND)
