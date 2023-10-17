from django.db.models import Count
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from apps.post import models, serializers, mixins, permissions



class StandardPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """Viewset for posts. List is sorted by creation date by default (?sort=new).
    Query parameter 'sort' can be set to 'hot' to sort by upvotes
    """ 
    permission_classes = (permissions.AuthorSuperOrReadOnly,)
    pagination_class = StandardPostPagination

    queryset = (
        models.Post.objects
        .select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all())

    serializer_class = serializers.PostModelSerializer

    def list(self, request, *args, **kwargs):
        """Overwrite list method to have different sorting depending on
        the queryparameter 'sort'
        """
        sort = self.request.GET.get("sort", "new")
        if sort == "new":
            self.queryset = (models.Post.objects
                .select_related("user_id", "cat_id")
                .prefetch_related("tags")
                .all()
                .order_by('-created_at'))
        elif sort == "hot":
            self.queryset = (models.Post.objects
                .select_related("user_id", "cat_id")
                .prefetch_related("tags")
                .annotate(rating=Count('userUpVotes', distinct=True) -
                            Count('userDownVotes', distinct=True),
                            upvotes=Count('userUpVotes'))
                .order_by('-rating', '-upvotes'))
        return super().list(self, request, *args, **kwargs)

    @action(detail=True, methods=['GET'], url_path='comments')
    def comments(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.comment_set.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CommentModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
