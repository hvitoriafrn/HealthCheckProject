from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('session/<int:session_id>/question/<int:question_number>/', views.voting_session_view, name='voting_session'),
]
