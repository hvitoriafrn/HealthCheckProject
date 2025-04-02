from django.shortcuts import render


'''
Stuff written by Vitoria. TBC 
def vote_home(request):
    return render(request, 'voting/home.html')

def submit_vote(request):
    return render(request, 'voting/submit.html')

def view_results(request):
    return render(request, 'voting/results.html')
'''


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import VotingSession, Question, Vote
from django.contrib import messages

@login_required
def dashboard(request):
    """Show pending and completed voting sessions."""
    pending_sessions = VotingSession.objects.filter(users=request.user).exclude(submitted_by=request.user)
    completed_sessions = VotingSession.objects.filter(submitted_by=request.user)
    
    return render(request, 'voting/dashboard.html', {
        'pending_sessions': pending_sessions,
        'completed_sessions': completed_sessions
    })

@login_required
def voting_session(request, session_id, question_index=0):
    """Display a single question for voting."""
    session = get_object_or_404(VotingSession, id=session_id, users=request.user)
    questions = Question.objects.all()
    
    # If the session is already submitted, prevent access
    if session.is_completed_by_user(request.user):
        messages.warning(request, "You have already submitted this session.")
        return redirect('dashboard')

    if question_index >= len(questions) or question_index < 0:
        return redirect('voting_session', session_id=session.id, question_index=0)

    question = questions[question_index]

    # Get existing vote, if any
    vote = Vote.objects.filter(user=request.user, session=session, question=question).first()

    if request.method == "POST":
        choice = request.POST.get("choice")
        comment = request.POST.get("comment", "")

        if choice in ['green', 'amber', 'red']:
            if vote:
                vote.choice = choice
                vote.comment = comment
                vote.save()
            else:
                Vote.objects.create(user=request.user, session=session, question=question, choice=choice, comment=comment)
        
        # Next or Previous navigation
        if "next" in request.POST and question_index + 1 < len(questions):
            return redirect('voting_session', session_id=session.id, question_index=question_index + 1)
        elif "previous" in request.POST and question_index > 0:
            return redirect('voting_session', session_id=session.id, question_index=question_index - 1)

    return render(request, 'voting/voting_session.html', {
        'session': session,
        'question': question,
        'question_index': question_index,
        'total_questions': len(questions),
        'vote': vote
    })

@login_required
def summary_view(request, session_id):
    """Show all answered questions before final submission."""
    session = get_object_or_404(VotingSession, id=session_id, users=request.user)
    questions = Question.objects.all()
    votes = Vote.objects.filter(user=request.user, session=session)

    if session.is_completed_by_user(request.user):
        messages.warning(request, "You have already submitted this session.")
        return redirect('dashboard')

    if request.method == "POST":
        # Final submission
        session.submitted_by.add(request.user)
        messages.success(request, "Your responses have been submitted successfully.")
        return redirect('dashboard')

    return render(request, 'voting/summary.html', {
        'session': session,
        'questions': questions,
        'votes': {v.question.id: v for v in votes}  # Dictionary for easy lookup
    })
