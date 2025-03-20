from django.shortcuts import render

# Create your views here.

def vote_home(request):
    return render(request, 'voting/home.html')

def submit_vote(request):
    return render(request, 'voting/submit.html')

def view_results(request):
    return render(request, 'voting/results.html')
