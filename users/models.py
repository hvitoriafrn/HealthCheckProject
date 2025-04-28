from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, role, userFirstName, userLastName, userTeam=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            userRole=role,
            userFirstName=userFirstName,
            userLastName=userLastName,
            userTeam=userTeam,
            is_staff=False,
            is_active=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(
            email=email,
            password=password,
            role=extra_fields.get('userRole', 'senior_manager'),
            userFirstName=extra_fields.get('userFirstName', 'Admin'),
            userLastName=extra_fields.get('userLastName', 'User'),
            userTeam=extra_fields.get('userTeam', None)
        )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    userFirstName = models.CharField(max_length=50)
    userLastName = models.CharField(max_length=50)
    userRole = models.CharField(
        max_length=30,
        choices=[
            ('engineer', 'Engineer'),
            ('leader', 'Team Leader'),
            ('dept_leader', 'Department Leader'),
            ('senior_manager', 'Senior Manager')
        ],
        blank=False,
        null=False
    )
    userTeam = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('team1', 'Team 1'),
            ('team2', 'Team 2'),
            ('team3', 'Team 3'),
        ]
    )
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userFirstName', 'userLastName']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.userID} - {self.userFirstName}- {self.email} - {self.userRole} - {self.userTeam or 'No team'}"