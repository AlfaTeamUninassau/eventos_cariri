from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Nome do usuário. Letras, dígitos e @/./+/-/_ apenas',
        validators=[username_validator]
    )
    email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    phone = models.CharField(
        max_length=100
    )
    city = models.CharField(
        max_length=100,
        choices=[
            ('JDO', 'Juazeiro do Norte'),
            ('CRT', 'Crato'),
            ('BRB', 'Barbalha'),
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
        ],
        default='JDO',
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.name