# this page was created by H Vitoria Almeida Franca, w1938811

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
#starting by registering the custom user model I created
class CustomUserAdmin(UserAdmin):
    model = User

#what columns will be displayed for admin view
    list_display = (
        'email', 
        'userFirstName',
        'userLastName',
        'userRole',
        'is_staff',
        'is_superuser')  

# displays email first on the list
    ordering = ('email',)

 #fieldsets defines which fields show on the edit user page inside admin

    fieldsets = (
        ('Login Credentials', { 'fields': ('email', 'password')  }),
        ('Personal Info', { 'fields': ('userFirstName', 'userLastName', 'userRole') }),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions') }),
        )
    
    #fields when adding a new user through admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'userFirstName',
                'userLastName',
                'userRole',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'), 
        }),
    )
#allows search functionality
    search_fields = ('email','userRole','teamID')
 
