from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    AnalysisEventListView,
    EventApproveView,
    EventUpdateView,
    EventDeleteView,
    EventSearchView,
    EventSearchAjaxView,
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
    path('analysis/', AnalysisEventListView.as_view(), name='analysis_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('new/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('search/', EventSearchView.as_view(), name='event_search'),
    path('<int:pk>/approve/', EventApproveView.as_view(), name='event_approve'),
    path('search/ajax/', EventSearchAjaxView.as_view(), name='event_search_ajax'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
