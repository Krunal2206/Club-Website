from django import forms
from django.forms import ModelForm
from .models import Venue, Event

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name','address','zip_code','phone','web','email_address','venue_image')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': ''
        }
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Venue Name"}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': "Please Enter Venue Address"}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Venue Zip Code"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Venue Contact Number"}),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Venue Web URL"}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Venue Email Address"}),
        }

# For Admin user
class EventAdminForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'name': '',
            'event_date': 'YYYY:MM:DD HH:MM:SS',
            'venue': 'Please Enter Venue',
            'manager': 'Please Enter Event Manager',
            'attendees': 'Please Enter Event Attendees',
            'description': ''
        }
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Name"}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Date"}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Description"}),
        }

# For simple user
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','attendees','description')
        labels = {
            'name': '',
            'event_date': 'YYYY:MM:DD HH:MM:SS',
            'venue': 'Please Enter Venue',
            'attendees': 'Please Enter Event Attendees',
            'description': ''
        }
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Name"}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Date"}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Please Enter Event Description"}),
        }