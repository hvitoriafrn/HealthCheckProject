from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import Group
from .models import Session, Vote

@login_required
def dashboard(request):
    # Shows the list of sessions the user can still vote on
    pending_sessions = (
        Session.objects
               .filter(users=request.user)              # sessions you’re part of
               .exclude(submitted_by=request.user)      # but haven’t submitted yet
    )
    return render(request, 'voting/dashboard.html', {
        'pending_sessions': pending_sessions,           # pass them to the template
    })

@login_required
def session(request, session_id):
    # Load the session you clicked on
    session = get_object_or_404(Session, pk=session_id)
    questions = session.questions_included.all()        # all of the questions in that session

    # If you’ve already voted, show a “you already did this” page
    if session.is_completed_by_user(request.user):
        return render(request, 'voting/already_submitted.html', {
            'session': session
        })

    # If you just hit “submit”…
    if request.method == 'POST':
        for question in questions:
            # grab your colour choice and any comment
            choice  = request.POST.get(f"{question.pk}-colour")
            comment = request.POST.get(f"{question.pk}-comment", '').strip()
            # if it’s a valid choice, save or update your vote
            if choice in Vote.vote_options:
                Vote.objects.update_or_create(
                    user=request.user,
                    session=session,
                    question=question,
                    defaults={'choice': choice, 'comment': comment}
                )
        # mark that you have completed this session
        session.submitted_by.add(request.user)
        return redirect('voting:dashboard')             # then go back to the dashboard

    # Otherwise just show the voting form
    return render(request, 'voting/session.html', {
        'session':   session,
        'questions': questions,
    })

@login_required
def team_summary(request):
    # 1) grab all sessions, newest first
    sessions = Session.objects.order_by('-created_at')
    # 2) see if the user has picked one from the dropdown; otherwise default to the very latest
    sid = request.GET.get('session')
    current = get_object_or_404(Session, pk=sid) if sid else sessions.first()

    # 3) find the session just before that, if it exists
    prev = None
    if current and sessions.count() > 1:
        all_s = list(sessions)
        idx = all_s.index(current)
        if idx + 1 < len(all_s):
            prev = all_s[idx+1]

    # 4) did they check “show trends”? (on = True, off = False)
    show_trend = request.GET.get('show_trend') == 'on'

    # 5) define the three teams we care about
    group_names = ["Your Team", "Team Beta", "Team Gamma"]
    groups      = [Group.objects.get(name=n) for n in group_names]

    # 6) get all the questions for the selected session
    questions   = current.questions_included.all()

    # 7) The helper function: for any (session, question, group) find the majority colour + arrow
    def majority_for(sess, question, group):
        qs = (Vote.objects
                 .filter(session=sess, question=question, user__groups=group)
                 .values('choice')
                 .annotate(cnt=Count('id')))
        d = {d['choice']: d['cnt'] for d in qs}         # make {'green': 5, 'amber': 3, …}
        best = max(d, key=lambda k: d.get(k, 0), default='amber')
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
                prev_c, prev_a = cur_c, ''           # if no trend, same colour + no arrow
            cells.append({'cur': (cur_c,  cur_a), 'prev': (prev_c, prev_a)})
        rows.append({'team': name, 'cells': cells})

    # ─── PIE CHART DATA ──────────────────────────────────────────────
    # count up all votes this session, by choice
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
        line_data.append(round(green * 100 / total, 0))  # percent of green votes

    # 9) finally, hand all that data off to the template
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
