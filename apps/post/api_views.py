from rest_framework import viewsets

from apps.post import models, serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        models.Post.objects
        .select_related("user_id", "cat_id")
        .prefetch_related("tags")
        .all())

    serializer_class = serializers.PostModelSerializer
