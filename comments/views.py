from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .models import Comment


class CommentsCreateView(CreateView):
    model = Comment
    template_name = 'comments/comments.html'
    fields = ['comment']
    success_url = reverse_lazy('comments')
    context_object_name = 'comments'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)