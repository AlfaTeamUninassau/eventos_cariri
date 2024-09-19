
from django.contrib import admin
from django.urls import path, include
from users.views import login_view, logout_view, register_view
from events.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('events/', include('events.urls')),
    path('comments/', include('comments.urls')),
    path('reviews/', include('reviews.urls')),
    path('', HomeView.as_view(), name='home'),
]
