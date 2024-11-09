# reviews/forms.py
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(attrs={'id': 'rating-input'}),
            'comment': forms.Textarea(attrs={
                'placeholder': 'fale sobre sua avaliação...',
                'rows': 3,
                'class': 'w-full p-2 border rounded'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True