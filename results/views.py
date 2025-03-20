from django.shortcuts import render

# Create your views here.

def results_home(request):
    return render(request, 'results/home.html')

def summary(request):
    return render(request, 'results/summary.html')
