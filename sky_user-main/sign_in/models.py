from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=150)
    irst_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
