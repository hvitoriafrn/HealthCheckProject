from django.urls import path
from . import views
app_name = 'voting'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:session_id>', views.session, name='session'),
    path('summary/', views.team_summary,   name='summary'),

]
  