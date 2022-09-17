from re import T
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.TextField(max_length=300)
    zip_code = models.CharField('Zip Code',max_length=15,blank=True)
    phone = models.CharField('Contact Phone', max_length=25)
    web = models.URLField('Website Address',blank=True)
    email_address = models.EmailField('Email Address')
    owner = models.IntegerField('Owner ID',blank=False,default=1)
    venue_image = models.ImageField(upload_to='images/',null=True,blank=True) 
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,blank=True,null=True)
    manager = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(User,blank=True,related_name="attendees")
    approved = models.BooleanField('Approved',default=False)

    def __str__(self):
        return self.name

    @property
    def Left_days(self):
        today = date.today()
        event_date = self.event_date.date()
        days = event_date - today
        days_stripped = str(days).split(',')[0]
        return days_stripped

    @property
    def Is_past(self):
        today = date.today()
        if self.event_date.date() < today:
            things = "Past"
        else:
            things = "Future"
        return things