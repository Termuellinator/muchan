from django.contrib import admin

from apps.post import models
# Register your models here.

class CustomPost(admin.ModelAdmin):
    list_display = (
        'title',
        'username',
        'category',
        'get_tags',
        'upvotes',
        'downvotes'
    )
    
    @admin.display(description="Tags")
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def upvotes(self, obj):
        return obj.userUpVotes.count()

    def downvotes(self, obj):
        return obj.userDownVotes.count()

class CustomComment(admin.ModelAdmin):
    list_display = (
        'username',
        'post_title',
        'short_body',
        'upvotes',
        'downvotes'
    )
    
    def upvotes(self, obj):
        return obj.userUpVotes.count()

    def downvotes(self, obj):
        return obj.userDownVotes.count()
    
class CustomPostTag(admin.ModelAdmin):
    list_display = (
        'title',
        'tag'
    ) 
    
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, CustomPost)
admin.site.register(models.Comment, CustomComment)
admin.site.register(models.PostTag, CustomPostTag)