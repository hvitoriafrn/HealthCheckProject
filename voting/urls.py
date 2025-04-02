from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('session/<int:session_id>/', views.voting_session, name='voting_session'),
    path('session/<int:session_id>/question/<int:question_index>/', views.voting_session, name='voting_session'),
    path('session/<int:session_id>/summary/', views.summary_view, name='summary_view'),
]
