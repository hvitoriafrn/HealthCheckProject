from django.shortcuts import redirect, render

# Create your views here.

def results_home(request):
    if request.user.is_authenticated:
        return render(request, 'results/home.html')
    else:
        return redirect('login')

def summary(request):
    if request.user.is_authenticated:
        return render(request, 'results/summary.html')
    else:
        return redirect('login')
