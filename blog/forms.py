from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta: # 필수 (Form은 View와 다르기 때문에)
        model = Comment # Comment와 연결되어있는 폼
        fields = ('content', )