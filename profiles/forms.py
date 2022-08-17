from .models import PostComments
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ('heading', 'email', 'body')
