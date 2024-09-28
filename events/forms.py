# events/forms.py
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Event, Location, EventImage
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class EventForm(forms.ModelForm):
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_price', 'name': 'price'})
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
            'age_group', 'privacy', 'ticket_type',
            'price', 'max_capacity'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_title', 'name': 'title', 'placeholder': 'qual será o nome do evento?'}),
            'date': forms.DateInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'type': 'date', 'id': 'id_date', 'name': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_time', 'name': 'time'}),
            'description': forms.Textarea(attrs={
    'class': 'w-full mt-1 p-2 border rounded',
    'id': 'id_description',
    'name': 'description',
    
    'placeholder': """Crie uma descrição detalhada do evento ex:
Junte-se a nós para uma experiência inesquecível na Tech Conference 2023!
Neste evento, reuniremos líderes da indústria, inovadores e entusiastas da tecnologia para três dias de palestras inspiradoras, workshops práticos e oportunidades de networking sem igual.
Programação:
Dia 1: Palestras de abertura e painéis de discussão
Dia 2: Workshops aprofundados e sessões temáticas
Dia 3: Eventos de networking e cerimônia de encerramento
O que esperar
Apresentações inovadoras sobre Inteligência Artificial, blockchain e Internet das Coisas
Demonstrações interativas dos mais recentes produtos tecnológicos
Oportunidades de conectar-se com profissionais da indústria e potenciais colaboradores
Acesso exclusivo à feira de emprego e sessões de recrutamento
"""
}),
            'category': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_category', 'name': 'category'}),
            'age_group': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_age_group', 'name': 'age_group'}),
            'privacy': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_privacy', 'name': 'privacy'}),
            'ticket_type': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_ticket_type', 'name': 'ticket_type'}),
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
            'price': {
                'max_digits': 'O preço não pode exceder R$9.999,00.',
            },
            'description': {
                'required': 'Este campo é obrigatório.',
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
                raise ValidationError(
                    "O horário do evento deve ser no futuro.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        print("EventForm initialized with errors: %s", self.errors)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_query', 'name': 'query'})
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] += ' border-red-500'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['cep', 'street', 'number', 'neighborhood', 'city', 'state']
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_cep', 'name': 'cep', 'placeholder': 'Digite o CEP para preencher automaticamente os campos abaixo'}),
            'street': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_street', 'name': 'street'}),
            'number': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded', 'id': 'id_number', 'name': 'number', 'placeholder': 'Digite o número do local'}),
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
        image = self.cleaned_data.get('images', None)

        if image:
            max_image_size = 10 * 1024 * 1024  # 10MB

            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise ValidationError(
                    f'O arquivo {image.name} não é uma imagem válida.')
            if image.size > max_image_size:
                raise ValidationError(
                    f'O arquivo {image.name} excede o tamanho máximo de 10MB.')

        return image
