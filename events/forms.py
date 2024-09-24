# events/forms.py
from django import forms
from .models import Event, Location, EventImage
from django.core.exceptions import ValidationError
import magic
from moviepy.editor import VideoFileClip

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['cep', 'street', 'number', 'neighborhood', 'city', 'state']
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'street': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'number': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'neighborhood': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'city': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'state': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
        }

class EventForm(forms.ModelForm):
    tickets = forms.IntegerField(
        min_value=1,
        max_value=500000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'})
    )
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'})
    )

    class Meta:
        model = Event
        fields = [
            'title', 'date', 'time', 'description', 'category',
            'age_group', 'privacy', 'ticket_type', 'tickets',
            'price', 'max_capacity'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'time': forms.TimeInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'date': forms.DateInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'category': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'age_group': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'privacy': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'ticket_type': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'tickets': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'price': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
        }
        error_messages = {
            'title': {
                'required': 'Este campo é obrigatório.',
            },
            'date': {
                'required': 'Este campo é obrigatório.',
            },
            'tickets': {
                'required': 'Este campo é obrigatório.',
                'max_value': 'A quantidade de ingressos não pode exceder 500.000.',
                'min_value': 'A quantidade de ingressos deve ser pelo menos 1.',
            },
            'price': {
                'max_digits': 'O preço não pode exceder R$9.999,00.',
            },
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class EventImageForm(forms.Form):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    def clean_images(self):
        files = self.files.getlist('images')
        max_image_size = 10 * 1024 * 1024  # 10MB
        max_upload_count = 5  # Máximo de 5 imagens

        if len(files) > max_upload_count:
            raise ValidationError(f'Você pode enviar no máximo {max_upload_count} imagens.')

        for file in files:
            if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise ValidationError(f'O arquivo {file.name} não é uma imagem válida.')

            if file.size > max_image_size:
                raise ValidationError(f'O arquivo {file.name} excede o tamanho máximo de 10MB.')

        return files