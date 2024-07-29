from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                profile_picture=form.cleaned_data['profile_picture'],
                address_line1=form.cleaned_data['address_line1'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
                user_type=form.cleaned_data['user_type']
            )
            login(request, user)
            return redirect('user:home')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Print form errors to console
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('user:dashboard')
    else:
        form = AuthenticationForm()
    return render(request,'users/user_login.html',{'form':form})


@login_required(login_url='user:login')
def dashboard(request):
    user = request.user
    print(f"Logged in user: {user.username}")  # Debugging
    try:
        profile = Profile.objects.get(user=user)
        print(f"Profile found: {profile}")  # Debugging
    except Profile.DoesNotExist:
        profile = None
        print("No profile found for user:", user.username)  # Debugging
    return render(request, 'users/dashboard.html', {'profile': profile})


def user_home(request):
    return render(request,'home.html')