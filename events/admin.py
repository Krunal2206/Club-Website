from django.contrib import admin
from .models import Venue
from .models import Event
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Register your models here.

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ['name']
    list_filter = ('name', 'address')
    search_fields = ['name', 'address']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'attendees', 'manager', 'approved')
    list_display = ('name', 'venue', 'event_date')
    ordering = ['event_date']
    list_filter = ('name', 'event_date')