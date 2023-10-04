from rest_framework import serializers

from apps.user.serializers import UserModelSerializer, UserModelShortSerializer
from . import models


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class PostModelSerializer(serializers.ModelSerializer):
    cat_id = CategoryModelSerializer()
    tags = TagModelSerializer(many=True)
    user_id = UserModelSerializer()
    userUpVotes = UserModelShortSerializer(many=True)
    userDownVotes = UserModelShortSerializer(many=True)

    class Meta:
        model = models.Post

        fields = (
            "id", # names the same as in model
            "title",
            "image",
            "user_id",
            "cat_id",
            "tags",
            "userUpVotes",
            "userDownVotes",
            "created_at",
            "modified_at",
        )
