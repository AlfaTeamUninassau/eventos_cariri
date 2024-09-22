from django.db import models


class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PRIVACY_CHOICES = [
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado'),
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

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    date = models.DateTimeField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    age_group = models.CharField(max_length=50, choices=AGE_GROUP_CHOICES)
    privacy = models.CharField(max_length=50, choices=PRIVACY_CHOICES)
    ticket_type = models.CharField(max_length=50)
    tickets = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/')