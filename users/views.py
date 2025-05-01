# created by H Vitoria Almeida Franca, w1938811

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreateForm, UserProfileUpdateForm 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#This was created by H Vitoria Almeida Franca, w1938811

# Create your views here.
def home(request):
    return render(request, 'users/home.html')
 
def success(request):
        return render(request, 'users/success.html')


def register(request):
    #if the user is already logged in and they click this button, it will take them to the profile page.
    if request.user.is_authenticated:
        return redirect('profile')

    #showing the form for the user when the load the register page
    if request.method == 'GET':
        return render(request, 'users/register.html', 
        {'form':UserCreateForm()})
    
    #binding it to post request when the user submits
    form = UserCreateForm(request.POST)
    #checking if everything is valid and then enter the try block
    if form.is_valid():
        try: 
            #save to the databse
            user = form.save()
            
            #will redirect the user to their profile page 
            return redirect('success') #This will probably be changed to the dashboard or summary page
        
        except IntegrityError:
            #if the email is already registered, display an error message
            return render(request, 'users/register.html',
                              {'form': form, })
    else: 
        #if the form is not valid, display the following error
        return render(request, 'users/register.html',
                       {'form': form})


#login view
def login_view(request):
    #added this so that the user cannot get to the login page if they're already logged in.
    if request.user.is_authenticated:
        return redirect('/voting/')

    if request.method == "POST":
        #renders the login form when the user visits the following page (login)
        form = AuthenticationForm(request, data=request.POST)
        
        #if the form is valid, retrieves the user
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user) #logs them in
            return redirect('/voting/') #takes them to home page
        else:
            return render(request, 'users/login.html', {'form': form})
        
    return render(request, 'users/login.html', {'form':AuthenticationForm()})


#function for logout (was previously using it wrong)
def logout_view(request):
    #this logs the user out and then redirects them to home page
    auth_logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request, 'users/logout_success.html')


# This was created by: Faaizah Ahmed, w1974473 // although it was not implemented 
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

# This part was created by: Faaizah Ahmed, w1974473 
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

