from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    )
from .models import Comment
from django.shortcuts import redirect
from django.contrib import messages


class CommentsCreateView(CreateView):
    model = Comment
    template_name = 'comments/comments.html'
    fields = ['comment']
    context_object_name = 'comments'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Comentário criado com sucesso!')
        return super().form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('comments'))


class CommentsUpdateView(UpdateView):
    model = Comment
    template_name = 'comment_edit.html'
    fields = ['comment']
    context_object_name = 'comments'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_comments'] = Comment.objects.select_related('event', 'author').order_by('-created_at')[:5]  # Limit to 5 recent comments

        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'comentário editado com sucesso!')
        return super().form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})


class CommentsListView(ListView):
    model = Comment
    template_name = 'comments/comments.html'
    context_object_name = 'comments'
    paginate_by = 10
    ordering = '-created_at'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CommentsDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'
    context_object_name = 'comment'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.event.pk})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Comentário deletado com sucesso!')
        return redirect(success_url)