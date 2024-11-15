from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from .models import Review
from .forms import ReviewForm
from events.models import Event

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event_id = self.kwargs['event_id']
        
        # Verificar se já existe uma review deste usuário para este evento
        existing_review = Review.objects.filter(
            user=self.request.user,
            event_id=self.kwargs['event_id']
        ).exists()
        
        if existing_review:
            return HttpResponseBadRequest("Você já avaliou este evento.")
        
        try:
            return super().form_valid(form)
        except IntegrityError:
            return HttpResponseBadRequest("Você já avaliou este evento.")

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.kwargs['event_id']})

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Avaliação atualizada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)