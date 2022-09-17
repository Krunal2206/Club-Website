from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from members.form import RegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.core.mail import send_mail, BadHeaderError

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In Successfully.')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in, Try again...')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Successfully.')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration Successfully.')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'authenticate/register.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'authenticate/profile.html', {})
    else:
        messages.error(request, ('Login Required To Access This Page'))
        return redirect('login')

def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_update = UserUpdateForm(request.POST or None, instance=request.user)
            profile_update = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
            if user_update.is_valid() and profile_update.is_valid():
                user_update.save()
                profile_update.save()
                messages.success(request, ('Your profile has been updated successfully.'))
                return redirect('profile')
            
        else:
            user_update = UserUpdateForm(instance=request.user)
            profile_update = ProfileUpdateForm(instance=request.user.profile)
            
        return render(request, 'authenticate/update_profile.html', {
            'user_update': user_update,
            'profile_update': profile_update
        })
    else:
        messages.error(request, ('Login Required To Access This Page'))
        return redirect('login')

def send_feedback(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = request.POST.get('subject')
            email = request.POST.get('email')
            message = request.POST.get('message')
            if subject and email and message:
                try:
                    send_mail(subject, message, email, ['email@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, ('Thanks for your feedback!'))
                return redirect('profile')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            return render(request, 'authenticate/feedback.html', {})
    else:
        messages.error(request, ('Login Required To Access This Page'))
        return redirect('login')