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

# Copied from Maryam's repository:
@login_required
def team_summary(request):
    # 1) grab all sessions, newest first
    sessions = Session.objects.order_by('-created_at')
    # 2) see if the user has picked a session from the dropdown; 
    # otherwise pick the latest one
    sid = request.GET.get('session')
    current = get_object_or_404(Session, pk=sid) if sid else sessions.first()

    # 3) find the session just before that, if it exists
    prev = None
    if current and sessions.count() > 1:
        all_s = list(sessions)
        idx = all_s.index(current)
        if idx + 1 < len(all_s):
            prev = all_s[idx+1]

    # 4) did they check “show trends” (on = True, off = False)
    show_trend = request.GET.get('show_trend') == 'on'

    # 5) definiing the 3 teams 
    group_names = ["Your Team", "Team Beta", "Team Gamma"]
    groups      = [Group.objects.get(name=n) for n in group_names]

    # 6) get all the questions for the selected session
    questions   = current.questions_included.all()

    # 7) The helper function: for any (session, question, group) 
    # find the majority colour + arrow
    def majority_for(sess, question, group):
        qs = (Vote.objects
                 .filter(session=sess, question=question, user__groups=group)
                 .values('choice')
                 .annotate(cnt=Count('id')))
        # build a dictionary, make {'green': 5, 'amber': 3, …}
        d = {d['choice']: d['cnt'] for d in qs}    
        # pick teh colour with the highest count, otherwise as default set it to amber
        best = max(d, key=lambda k: d.get(k, 0), default='amber')
        # choose the arrow symbol for that colour
        arrow = {'green':'▲', 'amber':'▬', 'red':'▼'}[best]
        return best, arrow

    # 8) build one “row” per team, each with a list of (current, previous) cells
    rows = []
    for grp, name in zip(groups, group_names):
        cells = []
        for q in questions:
            cur_c,  cur_a  = majority_for(current, q, grp)
            if show_trend and prev:
                prev_c, prev_a = majority_for(prev,    q, grp)
            else:
                # if there's no trend, show the same colour + no arrow
                prev_c, prev_a = cur_c, ''           
            cells.append({'cur': (cur_c,  cur_a), 'prev': (prev_c, prev_a)})
        rows.append({'team': name, 'cells': cells})

    # ─── PIE CHART DATA ──────────────────────────────────────────────
    # count up all votes in this session, by colour
    raw = (Vote.objects
             .filter(session=current)
             .values('choice')
             .annotate(cnt=Count('id')))
    choice_counts = {r['choice']: r['cnt'] for r in raw}
    pie_data   = [
      choice_counts.get('green', 0),
      choice_counts.get('amber', 0),
      choice_counts.get('red',   0),
    ]
    pie_labels = ['Good (Green)', 'Okay (Amber)', 'Bad (Red)']

    # ─── LINE CHART DATA ─────────────────────────────────────────────
    # look at the 4 most recent sessions, oldest first
    recent      = list(sessions.order_by('created_at')[:4])
    line_labels = [s.created_at.strftime("%d %b") for s in recent]
    line_data   = []
    for sess in recent:
        total = Vote.objects.filter(session=sess).count() or 1
        green = Vote.objects.filter(session=sess, choice='green').count()
        # percentage of green votes
        line_data.append(round(green * 100 / total, 0))  

    # 9) finally, hand all that data off to the vote_summary template
    return render(request, 'voting/vote_summary.html', {
        'sessions':        sessions,
        'current_session': current,
        'show_trend':      show_trend,
        'questions':       questions,
        'rows':            rows,

        'pie_data':     pie_data,
        'pie_labels':   pie_labels,
        'line_labels': line_labels,
        'line_data':   line_data,
    })