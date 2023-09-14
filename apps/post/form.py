from django import forms

from .models import Category, Tag


class NewComment(forms.Form):
    """Form to create a new comment."""

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "comment-input",
                "placeholder": "Write your comment and be nice! :)",
            }
        )
    )


class NewPost(forms.Form):
    """Form to create a new post."""

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "title-input", "placeholder": "Enter a Title"}
        )
    )

    image = forms.ImageField(label="Image")

    categories = [(cat.id, cat.cat) for cat in Category.objects.all()]
    cat_id = forms.IntegerField(
        widget=forms.Select(choices=categories), label="Category"
    )

    tags_list = [[tag.id, tag.name] for tag in Tag.objects.all()]
    tags = forms.MultipleChoiceField(choices=tags_list, label="Tags")
