# This page was created and worked on by H Vitoria Almeida Franca, w1938811
#In collaboration with Pawel Krezel (student no W1837610)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

#Create your models here.

#Custom user manager to handle the users that register and the super user (django admin)
class CustomUserManager(BaseUserManager):
    #creates a regular user
    def create_user (self, email, password=None ,**extra_fields):
        #error in case a user doesn't enter an email
        if not email:
            raise ValueError("Email is required")
        
        extra_fields.get('is_staff',False),
        extra_fields.get('is_superuser', False),
        extra_fields.get('is_active', True)


        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        #with this, we use django to hash the password securely
        user.set_password(password)
        user.save(using=self._db) #saving the user
        return user 
    
    #Similarly, method to create a super user, although this is only through terminal at the moment 
    #(probably will keep it this way)
    def create_superuser(self, email, password=None, **extra_fields):
        #this is to ensure the super user has the necessary permisions
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True) #explicitly saying they're super users so they can do everything
        extra_fields.setdefault('is_active', True) 
        extra_fields.setdefault('userRole', 'admin')
        extra_fields.setdefault('userFirstName', 'Admin')
        extra_fields.setdefault('userLastName', 'User')

        
        return self.create_user(email=email, password=password, **extra_fields)
    
#this is the custom user model for the app (page)
class User(AbstractBaseUser, PermissionsMixin):
    #each user had a userID assigned to them when they register, like in the logical ERD 
    #so this basically is stating that plus also, auto increments when a user is created
    userID = models.AutoField(primary_key=True)

    #the basic attributes that is needed to create a user
    email= models.EmailField(unique=True)
    userLastName = models.CharField(max_length=50)
    userFirstName = models.CharField(max_length=50)
    #userRole is added because we do not need multiple register pages for each type of user
    #so here the user will choose one and depending on what they choose, they will view one thing or another!
    userRole = models.CharField (max_length=30,
        choices = [     
            ('engineer', 'Engineer'),
            ('leader','Team Leader'),
            ('dept_leader', 'Department Leader'),
            ('senior_manager', 'Senior Manager')
        ],
        blank=True, 
        null=True
        )
    
    #linking the team table with teamID as fk 
    teamID = models.ForeignKey('voting.Team', on_delete=models.SET_NULL, null=True, blank=True)

    #added this or i would not be able to access django admin 
    #is set to false because only our team will have this as 'true'
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )    
    #defining that 'username' is in fact, email
    USERNAME_FIELD = 'email'
    #specifying the required fields for all, although it's not explicitly said, password and email are also necessary
    REQUIRED_FIELDS = ['userFirstName','userLastName', 'userRole']

    #links it to the customer manager model that has been defined above
    objects = CustomUserManager()

    #displays user info in the admin pa
    def __str__(self):
        return f"{self.userID} - {self.email} - {self.userRole}"
