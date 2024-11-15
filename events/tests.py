from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from users.models import User
from .models import Event, Location, EventImage
from .forms import EventForm, LocationForm, EventImageForm
from datetime import timedelta

class EventModelTest(TestCase):
    def setUp(self):
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Criar localização de teste
        self.location = Location.objects.create(
            cep='63050-000',
            street='Rua Teste',
            number='123',
            neighborhood='Centro',
            city='Juazeiro do Norte',
            state='CE'
        )
        
        # Criar evento de teste
        future_date = timezone.now() + timedelta(days=1)
        self.event = Event.objects.create(
            title='Evento Teste',
            description='Descrição teste',
            date=future_date,
            time=future_date.time(),
            location=self.location,
            category='Cultura',
            age_group='livre',
            privacy='public',
            ticket_type='gratuito',
            max_capacity=100,
            creator=self.user,
            status='em_analise'
        )

    def test_event_creation(self):
        self.assertTrue(isinstance(self.event, Event))
        self.assertEqual(str(self.event), 'Evento Teste')
        
    def test_event_fields(self):
        self.assertEqual(self.event.creator, self.user)
        self.assertEqual(self.event.location, self.location)
        self.assertEqual(self.event.title, 'Evento Teste')
        
    def test_get_average_rating(self):
        self.assertEqual(self.event.get_average_rating(), 0)

class EventViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        self.location = Location.objects.create(
            cep='63050-000',
            street='Rua Teste',
            number='123',
            neighborhood='Centro',
            city='Juazeiro do Norte',
            state='CE'
        )
        
        future_date = timezone.now() + timedelta(days=1)
        self.event = Event.objects.create(
            title='Evento Teste',
            description='Descrição teste',
            date=future_date,
            time=future_date.time(),
            location=self.location,
            max_capacity=100,
            creator=self.user,
            status='aprovado'
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')

    def test_event_detail_view(self):
        response = self.client.get(reverse('event_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_event_create_view_get(self):
        """Testa se a página de criação de evento é acessível"""
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_event_create_view_form_render(self):
        """Testa se o formulário de criação de evento é renderizado corretamente"""
        response = self.client.get(reverse('event_create'))
        
        # Verifica se todos os formulários necessários estão no contexto
        self.assertIn('form', response.context)
        self.assertIn('location_form', response.context)
        self.assertIn('image_form', response.context)
        
        # Verifica se a página foi renderizada com sucesso
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        
        # Verifica se os campos necessários estão presentes no formulário
        form = response.context['form']
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('category', form.fields)
        self.assertIn('age_group', form.fields)
        self.assertIn('privacy', form.fields)
        self.assertIn('ticket_type', form.fields)
        self.assertIn('max_capacity', form.fields)

        # Verifica se os campos do formulário de localização estão presentes
        location_form = response.context['location_form']
        self.assertIn('cep', location_form.fields)
        self.assertIn('street', location_form.fields)
        self.assertIn('number', location_form.fields)
        self.assertIn('city', location_form.fields)
        self.assertIn('state', location_form.fields)

class EventFormsTest(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=1)

    def test_event_form_valid(self):
        form_data = {
            'title': 'Evento Teste',
            'description': 'Descrição teste',
            'date': self.future_date.date(),
            'time': self.future_date.time(),
            'category': 'Cultura',
            'age_group': 'livre',
            'privacy': 'public',
            'ticket_type': 'gratuito',
            'max_capacity': 100,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_past_date(self):
        past_date = timezone.now() - timedelta(days=1)
        form_data = {
            'title': 'Evento Teste',
            'description': 'Descrição teste',
            'date': past_date.date(),
            'time': past_date.time(),
            'category': 'Cultura',
            'max_capacity': 100,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_location_form_valid(self):
        form_data = {
            'cep': '63050-000',
            'street': 'Rua Teste',
            'number': '123',
            'neighborhood': 'Centro',
            'city': 'Juazeiro do Norte',
            'state': 'CE'
        }
        form = LocationForm(data=form_data)
        self.assertTrue(form.is_valid())
