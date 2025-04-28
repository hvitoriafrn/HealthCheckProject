from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreateForm, UserProfileUpdateForm 
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'users/home.html')

@login_required
def profile_view(request):
    user = request.user
    profile_form = UserProfileUpdateForm(
        request.POST or None,
        instance=user,
        initial={
            'userFirstName': user.userFirstName,
            'userLastName': user.userLastName,
            'email': user.email,
            'userRole': user.userRole
        }
    )
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileUpdateForm(
                request.POST,
                instance=user,
                initial={
                    'userFirstName': user.userFirstName,
                    'userLastName': user.userLastName,
                    'email': user.email,
                    'userRole': user.userTeam
                }
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')

    team_choices = [('team1', 'Team 1'), ('team2', 'Team 2'), ('team3', 'Team 3')]

    return render(request, 'users/profile.html', {
        'user': user,
        'team_choices': team_choices,
        'profile_form': profile_form,
        'password_form': password_form,
    })

@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        # Update the logged-in user's profile
        user = request.user
        if field == "name":
            user.userFirstName = value
        elif field == "surname":
            user.userLastName = value
        elif field == "email":
            user.email = value
        elif field == "team":
            user.userTeam = value 
        user.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def success(request):
    return render(request, 'users/success.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html', {'form': UserCreateForm()})
    
    form = UserCreateForm(request.POST)
    if form.is_valid():
        try:
            user = form.save()
            auth_login(request, user)
            return redirect('success')
        except IntegrityError:
            messages.error(request, "A user with this email already exists.")
            return render(request, 'users/register.html', {'form': form})
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            auth_login(request, user)
            return redirect("profile")
        return render(request, "users/login.html", {"error": "Invalid email or password."})
    return render(request, "users/login.html")

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def team_summary_view(request):
    # Placeholder data for voting summary
    session = request.GET.get('session', 'session1')  # Default to session1
    voting_data = [
        {"question": "Delivering Value", "current_vote": "green", "trend": "arrow-up"},
        {"question": "Easy to Release", "current_vote": "amber", "trend": "arrow-down"},
        {"question": "Learning", "current_vote": "green", "trend": "rectangle"},
        {"question": "Pawns or Players", "current_vote": "red", "trend": "arrow-down"},
        {"question": "Teamwork", "current_vote": "green", "trend": "arrow-up"},
        {"question": "Health of Codebase", "current_vote": "amber", "trend": "rectangle"},
        {"question": "Mission", "current_vote": "green", "trend": "arrow-up"},
        {"question": "Speed", "current_vote": "red", "trend": "arrow-down"},
        {"question": "Suitable Process", "current_vote": "amber", "trend": "arrow-up"},
        {"question": "Support", "current_vote": "green", "trend": "rectangle"},
    ]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"voting_data": voting_data})


    return render(request, 'users/team_summary.html', {"voting_data": voting_data})