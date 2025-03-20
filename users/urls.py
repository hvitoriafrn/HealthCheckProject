from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Django's built-in authentication views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile, name='profile'),  # User profile
    path('register/', views.register, name='register'),  # User registration
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),  # Logout page
]