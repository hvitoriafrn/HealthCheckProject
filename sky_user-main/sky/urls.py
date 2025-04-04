from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('sign_in.urls')),
    path('admin/', admin.site.urls),
]
