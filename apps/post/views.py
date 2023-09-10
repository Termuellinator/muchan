from django.shortcuts import render, redirect

from .models import Post, Comment, PostTag, Category, Tag
from apps.user.models import User
from .form import NewComment, NewPost
# Create your views here.

def home_page(request):
    """Home Page with the 10 most recent posts displayed
    """
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
    """Display the detailed page of a specific post.
    
    Offers the possibility to post a comment for that post.

    Args:
        id (int): the id of the post to be displayed
    """
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
        
def new_post(request):
    """Display the page to create a new post.
    On successful creation, redirects to the detail page for that post.
    """
    if request.method == "GET":
        form = NewPost()
        return render(
            request=request,
            template_name="post/new_post.html",
            context={'form': form},
        )
    else:
        form = NewPost(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            data = form.cleaned_data
            print(data)            
            created_post = Post.objects.create(
                user_id = User.objects.get(pk=data['user_id']), 
                title = data['title'], 
                image = data.get('image'),
                cat_id = Category.objects.get(pk=data['cat_id']))
            created_post.save()
            for tag in data["tags"]:
                PostTag.objects.create(post_id=created_post, 
                                            tag_id=Tag.objects.get(pk=tag))
            return redirect('post-detail', created_post.id)
        return render(
            request=request,
            template_name="post/new_post.html",
            context={'form': form},
        )