from django.shortcuts import render

from .models import Post, Comment
from apps.user.models import User
from .form import NewComment
# Create your views here.

def home_page(request):
    posts = (Post.objects
            .select_related("user_id", "cat_id")
            .prefetch_related("tags")
            .all()
            .order_by('-created_at')[:10])

    context = {
        "posts": posts
    }
    return render(
        request=request, 
        template_name="index.html", 
        context=context
    )

def post_page(request, id):
    post = (Post.objects
            .select_related("user_id", "cat_id")
            .prefetch_related("tags")
            .get(pk=id))
    comments = (Comment.objects
                .select_related("user_id")
                .all()
                .filter(post_id = id)
                .order_by('-created_at'))
    
    context = {
        "title": post.title,
        "username": post.user_id.username,
        "image": post.image.url,
        "upvotes": post.userUpVotes.count(),
        "downvotes": post.userDownVotes.count(),
        "category": post.cat_id.cat,
        "tags": ", ".join([tag.name for tag in post.tags.all()]),
        "comments": comments
    }
    
    if request.method == "GET":
        form = NewComment()
        context["form"] = form
        return render(
            request=request, 
            template_name="post/post.html", 
            context=context
        )
    else:
        form = NewComment(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_comment = Comment.objects.create(
                user_id = User.objects.get(pk=data['user_id']),
                post_id = post,
                body = data["body"]
            )
            form = NewComment()
            context["form"] = form
            return render(
                request=request, 
                template_name="post/post.html", 
                context=context
            )
        return render(
            request=request, 
            template_name="post/post.html", 
            context=context
        )