from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'date': forms.DateTimeInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
        }
        error_messages = {
            'title': {
                'required': 'Este campo é obrigatório.',
            },
            'date': {
                'required': 'Este campo é obrigatório.',
            },
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # Adiciona classe de erro aos campos que não forem preenchidos
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class EventImageForm(forms.Form):
    images = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}), required=True)