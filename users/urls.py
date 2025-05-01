# This was created and mostly handled by H Vitoria Almeida Franca, w1938811 

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Django's built-in authentication views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.profile_view, name='profile'),  
    path('register/', views.register, name='register'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('logout_success/', views.logout_success, name='logout_success'),  # Logout page
    path('success/', views.success, name='success'),
    #password reset paths 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/resetPassword/reset_form.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/resetPassword/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/resetPassword/reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/resetPassword/reset_complete.html'),name='password_reset_complete'),
    #path to the view summary (unused)
    path("update-profile/", views.update_profile, name="update_profile"),
]
