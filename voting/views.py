from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VotingSession, QuestionTemplate, Vote
from .forms import VoteForm

@login_required
def dashboard(request):
    sessions = VotingSession.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'sessions': sessions})

@login_required
def voting_session_view(request, session_id, question_number):
    session = get_object_or_404(VotingSession, id=session_id, user=request.user)
    # Get the specific question by its number
    question = get_object_or_404(QuestionTemplate, number=question_number)
    
    # Check if a vote already exists for this question in the session
    vote_instance = Vote.objects.filter(voting_session=session, question_template=question).first()

    if request.method == 'POST':
        form = VoteForm(request.POST, instance=vote_instance)
        if form.is_valid():
            vote_obj = form.save(commit=False)
            vote_obj.voting_session = session
            vote_obj.question_template = question
            vote_obj.save()
            # Decide on navigation based on the button clicked
            if 'next' in request.POST:
                return redirect('voting_session', session_id=session.id, question_number=question_number + 1)
            elif 'prev' in request.POST:
                return redirect('voting_session', session_id=session.id, question_number=question_number - 1)
            elif 'save' in request.POST:
                # Optionally update session state if needed
                return redirect('dashboard')
    else:
        form = VoteForm(instance=vote_instance)

    context = {
        'session': session,
        'question': question,
        'form': form,
    }
    return render(request, 'voting_session.html', context)
