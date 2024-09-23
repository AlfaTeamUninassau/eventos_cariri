from django import forms
from .models import Event, EventImage, Location
from django.core.exceptions import ValidationError
import magic


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
    tickets = forms.IntegerField(min_value=1, max_value=500000, required=True, widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}))
    price = forms.DecimalField(max_digits=7, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}))

    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'location', 'age_group', 'privacy', 'ticket_type', 'tickets', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'date': forms.DateTimeInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'location': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'age_group': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'privacy': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'ticket_type': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
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
                'max_digits': 'O preço não pode exceder R$ 9.999,00.',
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

    def clean_images(self):
        files = self.files.getlist('images')
        max_image_size = 10 * 1024 * 1024  # 10MB
        max_video_duration = 60  # 1 minuto

        for file in files:
            if file.size > max_image_size:
                raise ValidationError(f'A imagem {file.name} excede o tamanho máximo de 10MB.')

            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file.read(1024))
            file.seek(0)

            if file_type.startswith('video/'):
                from moviepy.editor import VideoFileClip
                clip = VideoFileClip(file.temporary_file_path())
                if clip.duration > max_video_duration:
                    raise ValidationError(f'O vídeo {file.name} excede a duração máxima de 1 minuto.')

        return files