from django.contrib import admin

# Register your models here.

from .models import Event
from .models import EventImage
from .models import Location


admin.site.register(Event)