from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_home, name='vote_home'),  # Voting home page
    path('submit/', views.submit_vote, name='submit_vote'),  # Vote submission page
    path('results/', views.view_results, name='view_results'),  # View results page  
     path('choose-session/', views.choose_session, name='choose_session'),  # Voting sessions
    path('vote-summary/', views.vote_summary, name='vote_summary'),  # View summary  
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard view
]
