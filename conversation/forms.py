from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'file')

    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Comment...',
        'class': 'w-1/3 h-20 py-4 px-6 rounded-xl border',
    }))

    file = forms.FileField(required=False)    