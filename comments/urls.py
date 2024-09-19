from django.urls import path
from .views import CommentsCreateView

urlpatterns = [
    path('', CommentsCreateView.as_view(), name='comments'),
]
