from django.shortcuts import render
from events.models import Event, EventImage
from django.urls import reverse_lazy
from .forms import EventForm, EventImageForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

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
        if self.request.POST:
            context['image_form'] = EventImageForm(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = EventImageForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        if image_form.is_valid():
            event = form.save(commit=False)
            event.save()
            for file in self.request.FILES.getlist('images'):
                EventImage.objects.create(event=event, image=file)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)