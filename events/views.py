#events.views.py
from django.shortcuts import render
from events.models import Event, EventImage, Location
from django.urls import reverse_lazy
from .forms import EventForm, EventImageForm, LocationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
import logging


logger = logging.getLogger(__name__)


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'home'


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(FormView):
    template_name = 'create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['image_form'] = EventImageForm(self.request.POST, self.request.FILES)
            context['location_form'] = LocationForm(self.request.POST)
        else:
            context['image_form'] = EventImageForm()
            context['location_form'] = LocationForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        location_form = context['location_form']

        if form.is_valid():  # Verifica o formulário principal primeiro
            location = location_form.save()
            event = form.save(commit=False)
            event.location = location
            event.status = Event.EM_ANALISE
            event.save()

            if image_form.is_valid():  # Só processa as imagens se o formulário de imagem for válido
                for file in image_form.cleaned_data['images']:  # Usa cleaned_data para acesso seguro
                    EventImage.objects.create(event=event, image=file)
                messages.success(self.request, 'Evento criado com sucesso e está em análise.')
            else:
                messages.error(self.request, 'Erro ao criar o evento. Verifique os dados e tente novamente.')
                return self.form_invalid(form)  # Retorna inválido se houver erro nas imagens

            return super().form_valid(form)
        else:
            if not form.is_valid():
                logger.error(f"Erros no formulário principal: {form.errors}")
            if not location_form.is_valid():
                logger.error(f"Erros no formulário de localização: {location_form.errors}")
            messages.error(self.request, 'Erro ao criar o evento. Verifique os dados e tente novamente.')
            return self.form_invalid(form)
        
