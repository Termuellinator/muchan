from rest_framework import serializers

from apps.user.serializers import UserModelSerializer, UserModelShortSerializer
from . import models, validators


class CategoryModelSerializer(serializers.ModelSerializer):
    cat = serializers.CharField(validators=[
        validators.ValidateFuzzyUnique(
            queryset=models.Category.objects.all(),
            target_field="cat",
            source="serializer"          
        )
    ])
    class Meta:
        model = models.Category
        fields = "__all__"


class TagModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[
        validators.ValidateFuzzyUnique(
            queryset=models.Tag.objects.all(),
            target_field="name",
            source="serializer"          
        )
    ])
    class Meta:
        model = models.Tag
        fields = "__all__"


class CommentModelSerializer(serializers.ModelSerializer):
    user_id = UserModelSerializer()
    userUpVotes = UserModelShortSerializer(many=True)
    userDownVotes = UserModelShortSerializer(many=True)
    
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "body",
            "post_id",
            "user_id",
            "userUpVotes",
            "userDownVotes",
            "created_at",
            "modified_at",
        )


class PostModelSerializer(serializers.ModelSerializer):
    cat_id = CategoryModelSerializer()
    tags = TagModelSerializer(many=True)
    user_id = UserModelSerializer()
    userUpVotes = UserModelShortSerializer(many=True)
    userDownVotes = UserModelShortSerializer(many=True)
    comments = CommentModelSerializer(source="comment_set", many=True)

    class Meta:
        model = models.Post

        fields = (
            "id", # names the same as in model
            "title",
            "image",
            "user_id",
            "cat_id",
            "tags",
            "comments",
            "userUpVotes",
            "userDownVotes",
            "created_at",
            "modified_at",
        )
