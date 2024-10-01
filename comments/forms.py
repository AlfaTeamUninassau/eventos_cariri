# comments/forms.py
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded', 'placeholder': 'escreva sua opinião sobre o evento...'}),
        }
        labels = {
            'comment': '',
        }  # Remove o rótulo do campo de comentário
