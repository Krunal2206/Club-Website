from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)