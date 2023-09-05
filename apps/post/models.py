from django.db import models
from django.template.defaultfilters import truncatechars

from apps.core.models import CreatedModifiedDateTimeBase

# Create your models here.

class Category(CreatedModifiedDateTimeBase):
    cat = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.cat
    
class Tag(CreatedModifiedDateTimeBase):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Post(CreatedModifiedDateTimeBase):
    user_id = models.ForeignKey(
        "user.User", null=True, on_delete=models.SET_NULL)
    cat_id = models.ForeignKey(
        "post.Category", default=1, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=75)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    tags = models.ManyToManyField("post.Tag", through = "PostTag")
    userUpVotes = models.ManyToManyField(
        "user.User", blank=True, related_name='postUpVotes')
    userDownVotes = models.ManyToManyField(
        "user.User", blank=True, related_name='postDownVotes')
    # https://stackoverflow.com/questions/1528583/django-vote-up-down-method
    
    @property
    def username(self):
        return self.user_id.username
    
    @property
    def category(self):
        return self.cat_id.cat
    
    def __str__(self):
        return self.title
    
class PostTag(CreatedModifiedDateTimeBase):
    modified_at = None
    post_id = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    tag_id = models.ForeignKey("post.Tag", on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                "post_id",
                "tag_id",
                name = "post_tag_unique",
                violation_error_message="Tag already exist for post",
            )
        ]
    
    def title(self):
        return self.post_id.title
    
    def tag(self):
        return self.tag_id.name
        
    def __str__(self):
        return f"{self.post_id.title} - {self.tag_id.name}"
    
    
class Comment(CreatedModifiedDateTimeBase):
    post_id = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        "user.User", null=True, on_delete=models.SET_NULL)
    body = models.CharField(max_length=2000)
    userUpVotes = models.ManyToManyField(
        "user.User", blank=True, related_name='commentUpVotes')
    userDownVotes = models.ManyToManyField(
        "user.User", blank=True, related_name='commentDownVotes')
    # https://djangocentral.com/creating-comments-system-with-django/#building-comment-model
 
    @property
    def short_body(self):
        return truncatechars(self.body, 100)
    
    @property
    def username(self):
        return self.user_id.username
    
    @property
    def post_title(self):
        return self.post_id.title
    
    def __str__(self):
        return f"By {self.user_id.username} on {self.post_id.title}"