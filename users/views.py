from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def profile(request):
    return render(request, 'users/profile.html')

def register(request):
    #if request.method == 'GET':
        return render(request, 'users/register.html')
    #else: 
    #    if request.POST['password1'] == request.POST['password2']:
    #           user = User.objects.create_user(request.POST['email']),
    #           password = request.POST['password1']
    #           user.save()
    #           login (request, user)
    #           return redirect('home')
    #    else: 
    #       return render(request, 'users/register.html')
    #       {'form':UserCreationForm,
    #       'error':"Passwords do not match"})

#?
def login(request):
    return render(request, 'users/login.html')
#?
def logout(request):
    return render(request, 'users/logout.html')

#def signupUser(request):
  #  if request.method == 'GET':
  #      return render (request, 'users/register.html', {'form':UserCreationForm})
  #  else:
  #      if request.POST['password1'] == request.POST['passowrd2'] :
  #         user = User.objects.create_user(
  #         request.POST['username'], password = request.POST['password1'])
  #         user.save()
  #         login(request, user)
  #         return redirect('home')
#       else:
#           return render(request, 'users/register.html', 
#               {'form':UserCreationForm,
#               'error': 'Passwords do not match'})