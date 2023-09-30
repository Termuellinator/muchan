from typing import Optional
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.user.models import User
from .models import Post, Comment, PostTag, Category, Tag
from .form import NewComment, NewPost


# Create your views here.

class HomePageView(View):
    """Home Page with some number of posts displayed

    GET-Parameters:
        page(int): The page to display - Default 1
        posts_per_page(int): How many posts are displayed per page - Default 5
    """
    template_name = "index.html"
    
    def get(self, request):
        posts = (Post.objects
            .select_related("user_id", "cat_id")
            .prefetch_related("tags")
            .all()
            .order_by('-created_at'))
        
        page = request.GET.get("page", 1)
        posts_per_page = request.session.get("posts_per_page", 5)
        
        paginator = Paginator(posts, posts_per_page)
        paginated_posts = paginator.page(page)

        request.session["last_page"] = page

        form = AuthenticationForm()
        
        context = {
            "form": form,
            "paginated_posts": paginated_posts,
        }
        return render(
            request=request, 
            template_name=self.template_name, 
            context=context
        )
        
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # extract username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate the user
            user: Optional[User] = authenticate(
                username = username,
                password = password)
            # check if user was successfully authenticated
            if user is not None:
                # use the session to keep the authenticated users's id
                login(request, user)
                
                # Redirect the user to his profile page
                return redirect('profile')
            else:
                # TODO: what should happen if the user is not authenticated?
                pass
        else:
            self.error_message = "Sorry, something went wrong. Try again."
            
            return render(
            request=request,
            template_name=self.template_name,
            context={'form': form, 'error_message': self.error_message},
            )

class PostPageView(LoginRequiredMixin, View):
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
                user_id = request.user,
                post_id = Post.objects.get(pk=post_id),
                body = data["body"]
            )
            return redirect('post-detail', post_id)
        return render(
            request=request, 
            template_name=self.template_name,
            context=self.context
        )
        

class NewPostView(LoginRequiredMixin, View):
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
                user_id=request.user,
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


class UpVotePostView(LoginRequiredMixin, View):
    """Upvote a post for the currently logged in user
    """
    def get(self, request, post_id):
        self.post = Post.objects.get(pk=post_id)
        self.post.userUpVotes.add(request.user)

        return redirect(request.GET.get("next","home"))


class DownVotePostView(LoginRequiredMixin, View):
    """Downvote a post for the currently logged in user
    """
    def get(self, request, post_id):
        self.post = Post.objects.get(pk=post_id)
        self.post.userDownVotes.add(request.user)

        return redirect(request.GET.get("next","home"))


class UpVoteCommentView(LoginRequiredMixin, View):
    """Upvote a comment for the currently logged in user
    """
    def get(self, request, comment_id):
        self.comment = Comment.objects.get(pk=comment_id)
        self.comment.userUpVotes.add(request.user)

        return redirect(request.GET.get("next","home"))


class DownVoteCommentView(LoginRequiredMixin, View):
    """Downvote a comment for the currently logged in user
    """
    def get(self, request, comment_id):
        self.comment = Comment.objects.get(pk=comment_id)
        self.comment.userDownVotes.add(request.user)

        return redirect(request.GET.get("next","home"))