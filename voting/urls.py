# voting/urls.py
from django.urls import path
from . import views

app_name = 'voting'
urlpatterns = [
    # Make /voting/ go to the summary directly:
    path('',               views.dashboard_view, name='dashboard'), # changed from team_summary to dashboard so that voting sessions and view summary display different content
    path('<int:session_id>/', views.session,      name='session'),
    path('summary/',       views.team_summary,   name='summary'),
]
