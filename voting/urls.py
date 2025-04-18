from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_home, name='vote_home'),  # The main dashboard the user sees after logging in
   
]
