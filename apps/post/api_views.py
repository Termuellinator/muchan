from rest_framework import viewsets

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
    queryset = (models.Category.objects.all())

    serializer_class = serializers.CategoryModelSerializer