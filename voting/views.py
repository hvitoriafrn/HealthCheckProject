from django.shortcuts import render

# Create your views here.

def vote_home(request):
    return render(request, 'voting/home.html')

def submit_vote(request):
    return render(request, 'voting/submit.html')

def view_results(request):
    return render(request, 'voting/results.html')

def choose_session(request):
    return render(request, 'voting/choose_session.html')  #renders the choose session page

def vote_summary(request):
    return render(request, 'voting/vote_summary.html')  #renders the vote summary page

# Dashboard view to pass the user's role to the template
def dashboard_view(request):
    role = request.user.role  # Assuming `role` is a field on the user model or profile
    context = {
        'role': role,
    }
    return render(request, 'voting/dashboard.html', context)