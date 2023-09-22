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
    cat_id = forms.IntegerField(widget=forms.Select(), label="Category")
    tags = forms.MultipleChoiceField(label="Tags")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat_id"].widget.choices = (
            [(cat.id, cat.cat) for cat in Category.objects.all()])
        self.fields["tags"].choices = (
            [[tag.id, tag.name] for tag in Tag.objects.all()])

