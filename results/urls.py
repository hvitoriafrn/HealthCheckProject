from django.urls import path
from . import views

urlpatterns = [
    path('', views.results_home, name='results_home'),  # Results homepage
    path('summary/', views.summary, name='summary'),  # Summary of votes
]