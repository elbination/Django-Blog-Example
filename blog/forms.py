from .models import Comment
from django import forms


# Form: build standard forms
# ModelForm: build forms tied to model instances
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
