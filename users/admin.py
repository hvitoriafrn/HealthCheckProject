from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

#starting by registering the custom user model I created
admin.site.register(CustomUser)
