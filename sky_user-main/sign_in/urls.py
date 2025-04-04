from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.user_sign_in, name='sign in'),
]