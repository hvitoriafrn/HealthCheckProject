from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UserCreateForm
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth import logout as auth_logout



# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def profile(request):
    return render(request, 'users/profile.html')

def success(request):
    return render(request, 'users/success.html')

#User = get_user_model()

def register(request):
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
            #log the user once registered! (this line will be removed because we don't want this to happen)
            login(request,user)
            #save the session (keeps them logged in)
            user.save()
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


#login! 
def login_view(request):
    if request.method == "POST":
        #renders the login form when the user visits the following page (login)
        form = AuthenticationForm(request, data=request.POST)
        
        #if the form is valid, retrieves the user
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user) #logs them in
            return redirect('home') #takes them to home page
        else:
            return render(request, 'users/login.html', {'form': form})
        
    return render(request, 'users/login.html', {'form':AuthenticationForm})


#function for logout (was previously using it wrong)
def logout_view(request):
    #this logs the user out and then redirects them to home page
    auth_logout(request)
    return redirect('home')
    