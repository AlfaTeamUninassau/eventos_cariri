from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    
    # O username pode ser opcional
    username = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Nome de usuário. Letras, dígitos e @/./+/-/_ apenas',
        validators=[username_validator],
        unique=True,
        error_messages={'unique': 'Um usuário com este nome já existe.'},
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Digite seu nome e sobrenome'
        )
    email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
        )
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100, choices=[
        ('JDO', 'Juazeiro do Norte'),
        ('CRT', 'Crato'),
        ('BAR', 'Barbalha'),
        ('MIS', 'Missão Velha'),
        ('BRE', 'Brejo Santo'),
        ('JBA', 'Jardim'),
        ('JUA', 'Jati'),
        ('ASR', 'Assaré'),
        ('LAV', 'Lavras da Mangabeira'),
        ('ALT', 'Altaneira'),
        ('FAR', 'Farias Brito'),
        ('NOV', 'Nova Olinda'),
        ('PEN', 'Penaforte'),
        ('POR', 'Porteiras'),
        ('SAL', 'Salitre'),
        ('CAR', 'Caririaçu'),
        ('CAM', 'Campos Sales'),
        ('ARU', 'Araripe'),
        # Adicione as outras opções de cidade
    ], default='JDO')
    
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # O email será usado para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
