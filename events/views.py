#events.views.py
from django.shortcuts import render
from events.models import Event, EventImage, Location
from django.urls import reverse_lazy
from .forms import EventForm, EventImageForm, LocationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,
    RedirectView,
    DetailView,
    ListView,
    CreateView,
)
import logging


logger = logging.getLogger(__name__)


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'home'


class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 10


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(FormView):
    template_name = 'create.html'
    form_class = EventForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = EventImageForm()
        context['location_form'] = LocationForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = EventImageForm(self.request.POST, self.request.FILES)
        location_form = LocationForm(self.request.POST)

        if form.is_valid() and location_form.is_valid() and image_form.is_valid():
            location = location_form.save()
            event = form.save(commit=False)
            event.location = location
            event.status = Event.EM_ANALISE
            event.save()

            images = self.request.FILES.getlist('images')
            for image in images:
                if isinstance(image, InMemoryUploadedFile):
                    EventImage.objects.create(event=event, image=image)

            messages.success(self.request, 'Evento criado com sucesso e está em análise.')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['image_form'] = EventImageForm(self.request.POST, self.request.FILES)
        context['location_form'] = LocationForm(self.request.POST)
        messages.error(self.request, 'Erro ao criar o evento. Verifique os dados e tente novamente.')
        return self.render_to_response(context)