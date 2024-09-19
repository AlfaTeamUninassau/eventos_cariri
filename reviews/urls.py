from django.urls import path
from reviews.views import ReviewCreateView

urlpatterns = [
    path('', ReviewCreateView.as_view(), name='reviews'),
]
