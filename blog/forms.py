from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('id','title', 'content', 'image', 'category', 'tags')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
