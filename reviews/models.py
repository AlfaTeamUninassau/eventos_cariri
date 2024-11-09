# reviews/models.py
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')  # Um usuário só pode avaliar um evento uma vez

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.rating}/5"