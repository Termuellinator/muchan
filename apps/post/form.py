from django import forms

from .models import Post, Comment
from apps.user.models import User


class NewComment(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
            "class":"comment-input",
            "placeholder":"Write your comment and be nice! :)"}))
    
    users = [(user.id, user.username) for user in User.objects.all()]
    user_id = forms.IntegerField(widget=forms.Select(choices=users), label="User")