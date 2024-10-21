#events.models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from users.models import User
import logging


logger = logging.getLogger(__name__)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude field
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitude field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"


class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PRIVACY_CHOICES = [
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado'),
    ]

    INGRESSO_PAGO = 'pago'
    INGRESSO_GRATUITO = 'gratuito'
    INGRESSO_CHOICES = [
        (INGRESSO_PAGO, 'Pago'),
        (INGRESSO_GRATUITO, 'Gratuito'),
    ]

    LIVRE = 'livre'
    MAIS_12 = '+12'
    MAIS_16 = '+16'
    MAIS_18 = '+18'
    AGE_GROUP_CHOICES = [
        (LIVRE, 'Livre'),
        (MAIS_12, '+12 Anos'),
        (MAIS_16, '+16 Anos'),
        (MAIS_18, '+18 Anos'),
    ]
    CATEGORY_CHOICES = [
        ('Cultura', 'Cultura'),
        ('Esporte', 'Esporte'),
        ('Educacional', 'Educacional'),
        ('Música', 'Música'),
        ('Vaquejada', 'Vaquejada'),
        ('Literatura', 'Literatura'),
        ('Arte', 'Arte'),
        ('Palestra', 'Palestra'),
        ('Comida', 'Comida'),
        ('Lazer', 'Lazer'),
        ('Festival', 'Festival'),
        ('Festa', 'Festa'),
        ('Teatro', 'Teatro'),
        ('Conferência', 'Conferência'),
        ('Seminário', 'Seminário'),
        ('Workshop', 'Workshop'),
        ('Curso', 'Curso'),
        ('Reunião', 'Reunião'),
        ('Outro', 'Outro'),
    ]
    EM_ANALISE = 'em_analise'
    APROVADO = 'aprovado'
    REPROVADO = 'reprovado'
    STATUS_CHOICES = [
        (EM_ANALISE, 'Em Análise'),
        (APROVADO, 'Aprovado'),
        (REPROVADO, 'Reprovado'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=3000, null=False, blank=False)
    date = models.DateTimeField( null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, null=False, blank=False, default='other')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=False, blank=False)
    age_group = models.CharField(
        max_length=50, choices=AGE_GROUP_CHOICES, null=False, blank=False, default=LIVRE)
    privacy = models.CharField(
        max_length=50, choices=PRIVACY_CHOICES, null=False, blank=False, default=PUBLIC)
    ticket_type = models.CharField(
        max_length=50, choices=INGRESSO_CHOICES, null=False, blank=False, default=INGRESSO_GRATUITO)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    max_capacity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=EM_ANALISE
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        else:
            return 0 
    
    def save(self, *args, **kwargs):
        logger.debug("Saving event: %s", self.title)  # Log event title before saving
        print("Saving event: %s", self.title)  # Log event title before saving
        print("Event id: %s", self.id)  # Log event title before saving
        print("Event max_capacity: %s", self.max_capacity)  # Log event title before saving
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(
        Event, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        logger.debug("Saving event image: %s", self.image)  # Log event image before saving
        print("Saving event image: %s", self.image)  # Log event image before saving
        print("Event image: %s", self.event)  # Log event image before saving
        print("Event image id: %s", self.event.id)  # Log event image before saving
        super(EventImage, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.id
