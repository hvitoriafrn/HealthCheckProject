# voting/urls.py
from django.urls import path
from . import views

app_name = 'voting'
urlpatterns = [
    # what i had:
    # Make /voting/ go to the summary directly:
    path('',               views.dashboard, name='dashboard'),
    path('<int:session_id>/', views.session,      name='session'),
    #added by Maryam
    path('summary/',       views.team_summary,   name='summary'),
    # what yasmin did:
        #path('', views.vote_home, name='vote_home'),  # Voting home page
        #path('submit/', views.submit_vote, name='submit_vote'),  # Vote submission page
        #path('results/', views.view_results, name='view_results'),  # View results page  
        # path('choose-session/', views.choose_session, name='choose_session'),  # Voting sessions
    # path('summary/', views.vote_summary, name='summary'),  # View summary  
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard view
]

