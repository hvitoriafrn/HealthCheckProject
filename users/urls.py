from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Django's built-in authentication views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile, name='profile'),  # User profile
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout page
    path('success/', views.success, name='success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
