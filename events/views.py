from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventAdminForm
import csv
from django.db.models.functions import Lower
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    name = "Krunal"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = (int)(month_number)
    cal = HTMLCalendar().formatmonth(year,month_number)
    now = datetime.now()
    currunt_year = now.year
    time = now.strftime("%I:%M %p")

    event_list = Event.objects.filter(event_date__year=year, event_date__month=month_number)
    return render(request,'events/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "currunt_year":currunt_year,
        "time":time,
        "event_list":event_list
    })

def all_events(request):
    all_events = Event.objects.all().order_by(Lower('name').asc())
    paginator = Paginator(all_events, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = "a" * page_obj.paginator.num_pages

    return render(request,'events/events.html',{
        "page_obj": page_obj,
        "nums": nums,
    })

def add_event(request):
    submitted = False

    if request.method == "POST":
        if request.user.is_superuser:
            form = EventAdminForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
    else:
        if request.user.is_superuser:
            form = EventAdminForm()
        else:
            form = EventForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'events/add_event.html',{
        "form": form,
        "submitted": submitted
    })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventAdminForm(request.POST or None, instance=event)
        
    else:
        form = EventForm(request.POST or None, instance=event)
    
    if form.is_valid():
        form.save()
        return redirect('all_events')
    
    return render(request,'events/update_event.html',{
        'form': form,
        'event': event
    })

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        messages.success(request, ('Event deleted successfully.'))
        event.delete()
        return redirect('all_events')
    else:
        messages.error(request, ('You are not authorized to delete an event.'))
        return redirect('all_events')

def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request,'events/show_event.html',{
        "event": event,
    })

def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {
        'me': me,
        'events': events
    })
    else:
        messages.error(request, ('You are not authorized for this page.'))
        return redirect('home')

def searched_event(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains=searched)
        return render(request,'events/searched_events.html',{
            'searched': searched,
            'events': events
        })
    else:
        return render(request,'events/searched_events.html',{})

def all_venues(request):
    all_venues = Venue.objects.all().order_by(Lower('name').asc())
    paginator = Paginator(all_venues, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = "a" * page_obj.paginator.num_pages

    return render(request,'events/venues.html',{
        "page_obj": page_obj,
        "nums": nums,
    })

def add_venue(request):
    submitted = False

    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()

            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'events/add_venue.html',{
        "form": form,
        "submitted": submitted
    })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('all_venues')
    
    return render(request,'events/update_venue.html',{
        'form': form,
    })

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('all_venues')

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    events = venue.event_set.all()
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request,'events/show_venue.html',{
        "venue": venue,
        "venue_owner": venue_owner,
        "events": events
    })

def searched_venue(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request,'events/searched_venue.html',{
            'searched': searched,
            'venues': venues
        })
    else:
        return render(request,'events/searched_venue.html',{})

def venue_text(request):
    venues = Venue.objects.all()

    response = HttpResponse(content_type='text/plain',
        headers={'Content-Disposition': 'attachment; filename="venue.txt"'},)

    for venue in venues:
        response.writelines(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')

    return response

def venue_csv(request):
    venues = Venue.objects.all()

    response = HttpResponse(content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="venue.csv"'},)

    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Zip Code', 'Phone', 'Website', 'Email Address'])

    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response

def venue_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    
    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.setFont("Helvetica", 14)
    
    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    for line in lines:
        textobject.textLine(line)

    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='venue.pdf')

def admin_approval(request):
    event = Event.objects.all().count()
    venue = Venue.objects.all().count()
    user = User.objects.all().count()

    venues = Venue.objects.all()

    events = Event.objects.all()
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            events.update(approved = False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved = True)

            messages.success(request, 'Event Approved Successfully')
            return redirect('all_events')
        else:
            return render(request,'events/admin_approval.html',{
                'events': events,
                'venues': venues,
                'event': event,
                'venue': venue,
                'user': user
            })
    else:
        messages.success(request, 'You are not authorized to access this page.')
        return redirect('home')

def venue_events(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html', {
            'events': events,
        })
    else:
        messages.success(request, 'That Venue Has No Events At That Time')
        return redirect('admin_approval')