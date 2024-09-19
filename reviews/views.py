from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Review, Event
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('event_list')  # Redirecionar para a lista de eventos após a avaliação

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = Event.objects.get(pk=self.kwargs['event_id'])
        return super().form_valid(form)