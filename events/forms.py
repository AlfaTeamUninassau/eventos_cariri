# events/forms.py
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Event, Location, EventImage
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class EventForm(forms.ModelForm):
    tickets = forms.IntegerField(
        min_value=1,
        max_value=500000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_tickets', 'name': 'tickets'})
    )
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_price', 'name': 'price'})
    )
    
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'w-full mt-1 p-2 border rounded',
                'id': 'id_date',
                'name': 'date'
            }
        ),
        label="Data do Evento"
    )

    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'w-full mt-1 p-2 border rounded',
                'id': 'id_time',
                'name': 'time'
            }
        ),
        label="Horário do Evento"
    )

    class Meta:
        model = Event
        fields = [
            'title', 'date', 'time', 'description', 'category',
            'age_group', 'privacy', 'ticket_type', 'tickets',
            'price', 'max_capacity'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_title', 'name': 'title'}),
            'date': forms.DateInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'type': 'date', 'id': 'id_date', 'name': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_time', 'name': 'time'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_description', 'name': 'description'}),
            'category': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_category', 'name': 'category'}),
            'age_group': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_age_group', 'name': 'age_group'}),
            'privacy': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_privacy', 'name': 'privacy'}),
            'ticket_type': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_ticket_type', 'name': 'ticket_type'}),
            'tickets': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_tickets', 'name': 'tickets'}),
            'price': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_price', 'name': 'price'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_max_capacity', 'name': 'max_capacity'}),
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
        
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            event_datetime = timezone.make_aware(
                timezone.datetime.combine(date, time)
            )
            if event_datetime <= timezone.now():
                raise ValidationError("O horário do evento deve ser no futuro.")

        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        print("EventForm initialized with errors: %s", self.errors)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['cep', 'street', 'number', 'neighborhood', 'city', 'state']
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_cep', 'name': 'cep'}),
            'street': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_street', 'name': 'street'}),
            'number': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_number', 'name': 'number'}),
            'neighborhood': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_neighborhood', 'name': 'neighborhood'}),
            'city': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_city', 'name': 'city'}),
            'state': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_state', 'name': 'state'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'


class EventImageForm(forms.Form):
    images = forms.FileField(
        widget=ClearableFileInput(attrs={'id': 'id_images', 'name': 'images'}),
        required=False
    )

    class Meta:
        model = EventImage
        fields = ['images', 'event']

    def clean_images(self):
        # Access files from cleaned_data as Django processes it through request.FILES automatically
        image = self.cleaned_data.get('images')  # Now we're dealing with a single file

        if not image:
            raise ValidationError("No file was submitted. Check the encoding type on the form.")
        
        max_image_size = 10 * 1024 * 1024  # 10MB
        
        if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise ValidationError(f'O arquivo {image.name} não é uma imagem válida.')
        if image.size > max_image_size:
            raise ValidationError(f'O arquivo {image.name} excede o tamanho máximo de 10MB.')

        return image