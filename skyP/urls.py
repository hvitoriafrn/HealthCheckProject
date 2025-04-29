from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',    include('users.urls')),   #  home/login/register URLs
    path('voting/', include('voting.urls')),
    path('results/', include('results.urls')),
]

