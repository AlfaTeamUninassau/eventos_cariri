# events.views.py
from django.shortcuts import render
from events.models import Event, EventImage, Location
from .utils import get_lat_long
from django.urls import reverse_lazy
from .forms import EventForm, EventImageForm, LocationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.utils import timezone
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now(), status=Event.APROVADO).order_by('date')[:3]  # Limit to 6 events
        return context


class AnalysisEventListView(ListView):
    model = Event
    template_name = 'admin_events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(status=Event.EM_ANALISE)


class EventApproveView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.status = Event.APROVADO
        event.save()
        messages.success(request, 'Evento aprovado com sucesso.')
        return redirect('analysis_events')


class EventUpdateView(View):
    ...


@method_decorator(login_required, name='dispatch')
class EventDeleteView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        messages.success(request, 'Evento excluído com sucesso.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(status=Event.APROVADO)


class EventSearchView(ListView):
    model = Event
    template_name = 'base.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        event = Event.objects.get(pk=self.kwargs['pk'])
        search_query = event.title
        if search_query:
            return Event.objects.filter(title__icontains=search_query)
        else:
            return Event.objects.none()


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['similar_events'] = Event.objects.filter(
            category=event.category,
            date__gte=timezone.now(),
            status=Event.APROVADO
        ).exclude(id=event.id)[:4]
        return context


def upcoming_events_view(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now(), status=Event.APROVADO).order_by('date')
    
    return render(request, 'home.html', {'upcoming_events': upcoming_events})


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
            # Save the location data
            location = location_form.save(commit=False)

            # Prepare the full address to send to the geocoder
            address = f"{location.street}, {location.number}, {location.neighborhood}, {location.city}, {location.state}"

            # Get latitude and longitude using Nominatim
            latitude, longitude = get_lat_long(address)

            if latitude and longitude:
                location.latitude = latitude
                location.longitude = longitude
            else:
                # Handle case where geocoding fails
                messages.error(
                    self.request, 'Não foi possível obter a localização geográfica para o endereço fornecido.')
                return self.form_invalid(form)

            location.save()

            # Save the event and associate it with the location
            event = form.save(commit=False)
            event.location = location
            event.status = Event.EM_ANALISE

            # Make the event date and time timezone-aware
            event_datetime = timezone.make_aware(timezone.datetime.combine(
                form.cleaned_data['date'], form.cleaned_data['time']))
            event.date = event_datetime
            event.save()

            # Handle images
            images = self.request.FILES.getlist('images')
            if images:
                for image in images:
                    if isinstance(image, InMemoryUploadedFile):
                        EventImage.objects.create(event=event, image=image)

            messages.success(
                self.request, 'Evento criado com sucesso e está em análise.')
            return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['image_form'] = EventImageForm(
            self.request.POST, self.request.FILES)
        context['location_form'] = LocationForm(self.request.POST)
        messages.error(
            self.request, 'Erro ao criar o evento. Verifique os dados e tente novamente.')
        return self.render_to_response(context)
