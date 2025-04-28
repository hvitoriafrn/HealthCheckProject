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

    # If user already fully submitted this session, show a message
    if session.is_completed_by_user(request.user):
        return render(request, 'voting/already_submitted.html', {'session': session})

    if request.method == 'POST':
        action = request.POST.get('action')  # either 'save' or 'submit'

        # Save or update votes for every question present

        for question in questions:
            choice = request.POST.get(f"{question.pk}-colour")
            comment = request.POST.get(f"{question.pk}-comment", '').strip()

            if choice in Vote.vote_options:
                Vote.objects.update_or_create(
                    user=request.user,
                    session=session,
                    question=question,

                    defaults={'choice': choice, 'comment': comment}
                )

        if action == 'submit':
            # Final submission: mark as completed
            session.submitted_by.add(request.user)
            return redirect('voting:dashboard')

        # action == 'save' (or anything else): just re-load this session page
        return redirect('voting:session', session_id=session.id)

    # GET request: render session with any previously saved votes
    user_votes = Vote.objects.filter(user=request.user, session=session)
    votes_dict = {v.question_id: v for v in user_votes}

    context = {
        'session': session,
        'questions': questions,
        'questions_qty': questions.count(),
        'votes_dict': votes_dict,
    }
    return render(request, 'voting/session.html', context)
