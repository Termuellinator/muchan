from django.shortcuts import render

from .models import Post
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