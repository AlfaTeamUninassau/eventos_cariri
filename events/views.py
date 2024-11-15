# events.views.py
from django.shortcuts import render, get_object_or_404
from events.models import Event, EventImage, Location
from .utils import get_lat_long
from django.urls import reverse_lazy
from .forms import EventForm, EventImageForm, LocationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Min, Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.generic.edit import FormView
from comments.forms import CommentForm
from comments.models import Comment
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from reviews.forms import ReviewForm
from reviews.models import Review


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
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)


class EventSearchAjaxView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            events = Event.objects.filter(title__icontains=query, status=Event.APROVADO)
            results = [{'id': event.id, 'title': event.title} for event in events]
        else:
            results = []
        return JsonResponse(results, safe=False)


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now(), status=Event.APROVADO).order_by('date')[:3]  # 3 lasts events
        context['recent_comments'] = Comment.objects.select_related('event', 'author').order_by('-created_at')[:5]  # Limit to 5 recent comments

        return context


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = EventImageForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = EventImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            event = form.save(commit=False)
            event.save()
            if 'images' in self.request.FILES:
                EventImage.objects.filter(event=event).delete()
                for image in self.request.FILES.getlist('images'):
                    EventImage.objects.create(event=event, image=image)
            messages.success(self.request, 'Evento atualizado com sucesso.')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EventDeleteView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        if request.user == event.creator or request.user.is_superuser:
            event.delete()
            messages.success(request, 'Evento excluído com sucesso.')
            return redirect(self.request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseForbidden('Você não tem permissão para deletar este evento.')


class AboutView(TemplateView):
    template_name = 'about.html'


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            # Enviar email (ajuste as configurações de email no settings.py)
            send_mail(
                f'Mensagem de {name} - Eventos Cariri',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Sua mensagem foi enviada com sucesso!')
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            messages.error(request, 'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente mais tarde.')

        return render(request, 'about.html')

    return render(request, 'about.html')


class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.filter(status=Event.APROVADO).order_by('-date')
        category = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        location = self.request.GET.get('location')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        query = self.request.GET.get('query')

        if category:
            queryset = queryset.filter(category=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if location:
            queryset = queryset.filter(location__city__icontains=location)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [choice[0] for choice in Event.CATEGORY_CHOICES]
        context['locations'] = Location.objects.values_list('city', flat=True).distinct()
        context['selected_categories'] = self.request.GET.getlist('category')
        return context


class EventSearchView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Event.objects.filter(title__icontains=query, status=Event.APROVADO)
        else:
            return Event.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context


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
        context['comment_form'] = CommentForm()
        context['comments'] = event.comments.all()
        context['review_form'] = ReviewForm()

        # Verifica se o usuário já fez uma avaliação
        if self.request.user.is_authenticated:
            try:
                context['user_review'] = Review.objects.get(event=event, user=self.request.user)
            except Review.DoesNotExist:
                context['user_review'] = None

        context['reviews'] = event.review_set.all()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'rating' in request.POST:
            # Processamento do formulário de avaliação
            form = ReviewForm(request.POST)

            if form.is_valid():
                # Verifica se o usuário já avaliou o evento
                if Review.objects.filter(event=self.object, user=request.user).exists():
                    messages.error(request, 'Você já avaliou este evento.')
                    return self.render_to_response(self.get_context_data(form=form))
                
                review = form.save(commit=False)
                review.user = request.user
                review.event = self.object
                review.save()
                messages.success(request, 'Avaliação enviada com sucesso.')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                messages.error(request, 'Erro ao enviar a avaliação. Verifique os dados e tente novamente.')
                return self.render_to_response(self.get_context_data(form=form))
        else:
            # Processamento do formulário de comentário
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.event = self.object
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso!')
                return redirect('event_detail', pk=self.object.pk)
            else:
                messages.error(request, 'Erro ao adicionar comentário.')
                return self.render_to_response(self.get_context_data(comment_form=comment_form))

        return redirect('event_detail', pk=self.object.pk)


def upcoming_events_view(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now(), status=Event.APROVADO).order_by('date')
    
    return render(request, 'home.html', {'upcoming_events': upcoming_events})


class EventCreateView(FormView):
    template_name = 'create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')  # Alterado de 'home' para 'events'


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

            # Get latitude and longitude using the geocoder
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
            event.creator = self.request.user  # Definindo o campo creator

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
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['image_form'] = EventImageForm(
            self.request.POST, self.request.FILES)
        context['location_form'] = LocationForm(self.request.POST)
        messages.error(
            self.request, 'Erro ao criar o evento. Verifique os dados e tente novamente.')
        return self.render_to_response(context)
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})