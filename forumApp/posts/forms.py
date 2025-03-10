from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from forumApp.posts.models import Post, Comment


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a post'
            }
        )
    )


class CommentBaseForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Your Comment'
        }


class CommentCreateForm(CommentBaseForm):
    pass


class CommentEditForm(CommentBaseForm):
    pass


class CommentDeleteForm(CommentBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True
