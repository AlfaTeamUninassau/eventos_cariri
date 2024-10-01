from django.db import models
from events.models import Event
from users.models import User

# Create your models here.


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment