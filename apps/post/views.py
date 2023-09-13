from django.shortcuts import render, redirect
from django.views import View

from .models import Post, Comment, PostTag, Category, Tag
from apps.user.models import User
from .form import NewComment, NewPost


# Create your views here.

class HomePageView(View):
    """Home Page with the 10 most recent posts displayed
    """
    template_name = "index.html"
    
    def get(self, request):
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
            template_name=self.template_name, 
            context=context
        )

class PostPageView(View):
    """Display the detailed page of a specific post.
    
    Offers the possibility to post a comment for that post.
    """

    template_name = "post/post.html"

    def get(self, request, post_id):

        self.post_data = (Post.objects
                .select_related("user_id", "cat_id")
                .prefetch_related("tags")
                .get(pk=post_id))
        self.comments = (Comment.objects
                    .select_related("user_id")
                    .all()
                    .filter(post_id = post_id)
                    .order_by('-created_at'))

        self.context = {
            "title": self.post_data.title,
            "username": self.post_data.user_id.username,
            "image": self.post_data.image.url,
            "upvotes": self.post_data.userUpVotes.count(),
            "downvotes": self.post_data.userDownVotes.count(),
            "category": self.post_data.cat_id.cat,
            "tags": ", ".join([tag.name for tag in self.post_data.tags.all()]),
            "comments": self.comments
        }
        form = NewComment()
        self.context["form"] = form
        return render(
            request=request, 
            template_name=self.template_name, 
            context=self.context
        )
        
    def post(self, request, post_id):
        form = NewComment(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_comment = Comment.objects.create(
                user_id = User.objects.get(pk=data['user_id']),
                post_id = Post.objects.get(pk=post_id),
                body = data["body"]
            )
            return redirect('post-detail', post_id)
        return render(
            request=request, 
            template_name=self.template_name, 
            context=self.context
        )
        

class NewPostView(View):
    """Display the page to create a new post.
    On successful creation, redirects to the detail page for that post.
    """
    template_name = "post/new_post.html"
    
    def get(self, request):
        form = NewPost()
        return render(
            request=request,
            template_name=self.template_name,
            context={'form': form},
        )
    
    def post(self, request):
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            created_post = Post.objects.create(
                user_id=User.objects.get(pk=data['user_id']), 
                title=data['title'], 
                image=data.get('image'),
                cat_id=Category.objects.get(pk=data['cat_id'])
            )
            created_post.save()
            for tag in data["tags"]:
                PostTag.objects.create(
                    post_id=created_post, 
                    tag_id=Tag.objects.get(pk=tag)
                )
            return redirect('post-detail', created_post.id)
        return render(
            request=request,
            template_name=self.template_name,
            context={'form': form},
        )