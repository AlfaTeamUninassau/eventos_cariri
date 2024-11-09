from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('', ReviewCreateView.as_view(), name='reviews'),
    path('create/<int:event_id>/', ReviewCreateView.as_view(), name='review_create'),
    path('update/<int:pk>/', ReviewUpdateView.as_view(), name='review_update'),  # URL atualizada
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),  # URL atualizada
]
