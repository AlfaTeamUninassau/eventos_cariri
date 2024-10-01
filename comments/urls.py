from django.urls import path
from .views import CommentsCreateView, CommentsUpdateView, CommentsDeleteView

urlpatterns = [
    path("", CommentsCreateView.as_view(), name="comments"),
    path('edit/<int:pk>/', CommentsUpdateView.as_view(), name='comment_edit'),
    path('delete/<int:pk>/', CommentsDeleteView.as_view(), name='comment_delete'),
]
