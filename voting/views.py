from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Session, Question, Vote

@login_required
def dashboard(request):
    #query to find sessions that have not been completed by the logged in user
    pending_sessions = Session.objects.filter(users=request.user).exclude(submitted_by=request.user)
    context = {
        'user':request.user,
        'pending_sessions':pending_sessions
    }
    return render(request, 'voting/dashboard.html', context)

@login_required
def session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    questions = session.questions_included.all()

    # troubleshooting - if user already submitted this session
    if session.is_completed_by_user(request.user):
        return render(request, 'voting/already_submitted.html', {'session': session})

    # if the form was submitted
    if request.method == 'POST':
        for question in questions:
            choice = request.POST.get(f"{question.pk}-colour")
            comment = request.POST.get(f"{question.pk}-comment", '').strip()

            if choice in Vote.vote_options:
                Vote.objects.update_or_create(
                    user=request.user,
                    session=session,
                    question=question,
                    defaults={
                        'choice': choice,
                        'comment': comment
                    }
                )

        # Mark session as submitted and go back to the dashborad 
        session.submitted_by.add(request.user)
        return redirect('/voting/') 
    
    # if the form was not submitted and we need to render questions 
    context = {
        'session': session,
        'questions': questions
    }
    return render(request, 'voting/session.html', context)