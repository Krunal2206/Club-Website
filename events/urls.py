from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),

    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/<event_id>/', views.update_event, name='update_event'),
    path('delete_event/<event_id>/', views.delete_event, name='delete_event'),
    path('show_event/<event_id>/', views.show_event, name='show_event'),
    path('my_events/', views.my_events, name='my_events'),
    path('searched_event/', views.searched_event, name='searched_event'),

    path('all_venues/', views.all_venues, name='all_venues'),
    path('add_venue/', views.add_venue, name='add_venue'),
    path('update_venue/<venue_id>/', views.update_venue, name='update_venue'),
    path('delete_venue/<venue_id>/', views.delete_venue, name='delete_venue'),
    path('show_venue/<venue_id>/', views.show_venue, name='show_venue'),
    path('searched_venue/', views.searched_venue, name='searched_venue'),

    path('venue_text/', views.venue_text, name='venue_text'),
    path('venue_csv/', views.venue_csv, name='venue_csv'),
    path('venue_pdf/', views.venue_pdf, name='venue_pdf'),

    path('admin_approval/', views.admin_approval, name='admin_approval'),
    path('venue_events/<venue_id>/', views.venue_events, name='venue_events'),
]