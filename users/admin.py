from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
#starting by registering the custom user model I created
class CustomUserAdmin(UserAdmin):
    model = User

# what columns will be displayed for admin view
    list_display = (
        'email', 
        'userFirstName',
        'userLastName',
        'userRole',
        'is_staff',
        'is_superuser')  

# displaying email first on the list
    ordering = ('email',)

 # fieldsets will define which fields show on the edit user page inside admin

    fieldsets = (
     ('Login Credentials', {
         'fields': ('email', 'password') 
     }),
     ('Personal Info', {
        'fields': ('userFirstName', 'userLastName', 'userRole')
      }),
      ('Permissions', {
        'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )
       
       }),
    )
    search_fields = ('email','userRole','team')
 