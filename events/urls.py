from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    ApprovedEventListView,
    # EventUpdateView,
    # EventDeleteView
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
    path('approved-events/', ApprovedEventListView.as_view(), name='approved_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('new/', EventCreateView.as_view(), name='event_create'),
    # path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    # path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
