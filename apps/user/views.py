from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.post.models import Post
# Create your views here.


class UserProfileView(LoginRequiredMixin, View):
    """Show the users profile page if they are logged in."""

    template_name = "user/profile.html"

    def get(self, request):
        posts = (Post.objects
            .select_related("cat_id")
            .prefetch_related("tags")
            .all()
            .filter(user_id = request.user.id)
            .order_by('-created_at')[:10])
        
        context = {
            "posts": posts,
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )


class UserLogoutView(View):
    """Logout current user session and redirect to the home page"""

    def get(self, request):
        request.session.flush()
        return redirect("home")
