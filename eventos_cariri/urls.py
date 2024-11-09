from django.contrib import admin
from django.urls import path, include
from users.views import login_view, logout_view, register_view, profile_view, user_profile_view
from events.views import HomeView, AboutView, contact_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', profile_view, name='profile'),
    path('profile/<str:username>/', user_profile_view, name='user_profile'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('events/', include('events.urls')),
    path('comments/', include('comments.urls')),
    path('reviews/', include('reviews.urls')),
    path('sobre/', AboutView.as_view(), name='about'),
    path('contact/', contact_view, name='contact'),
    path('', HomeView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
