#This page was created by H Vitoria Almeida Franca, w1938811
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from django.core.exceptions import ValidationError

#This section was created by Faaizah Ahmed, w1974473
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userFirstName', 'userLastName', 'email', 'teamID', 'userRole']
        labels = {
            'userFirstName': 'First name',
            'userLastName': 'Last name',
            'email': 'Email address',
            'teamID': 'teamID',
            'userRole': 'Role'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['userRole'].widget.attrs['disabled'] = True

    def save(self, commit=True):
        # Get the existing user instance
        user = self.instance
        
        # Update fields
        user.userFirstName = self.cleaned_data['userFirstName']
        user.userLastName = self.cleaned_data['userLastName']
        user.email = self.cleaned_data['email']
        user.teamID = self.cleaned_data['teamID']
        
        # For disabled fields, use initial values
        user.userRole = self.initial.get('userRole') 
        
        if commit:
            user.save()
        return user

#user creation was handled and created by H Vitoria Almeida Franca, w1938811
class UserCreateForm(UserCreationForm):

    class Meta:
        #creating a custom model because django's uses username, not email :(
        model = User
        #fields where the user will input their details
        fields = [
            'userFirstName',
            'userLastName',
            'email',
            'userRole',
            'password1',
            'password2'
        ]
        #labels because the fields were showing all messed up!!!!!!
        labels = {
            'userFirstName': 'First name',
            'userLastName': 'Last name',
            'email': 'Email address',
            'userRole': 'Role',
            'password1': 'Password',
            'password2': 'Confirm password',
        }

    #constructor for the user creation
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        #loops thorugh the fields and adds bootstrap class for the style
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'})  

        #removes the default text from the password input fields 
        #to add our own errors according to our prototype
        for fieldname in ['password1','password2']:
              self.fields[fieldname].help_text = None
        
    #check if the email exists already in the databse
    def checkEmail(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email address is already registered")
            return email

    #defining the save method
    def save(self, commit=True):
        #to acces the data after it's been validated
        cleaned = self.cleaned_data
        #creates a new user instance using the model (logicalERD style)
        user = User.objects.create_user(
            email=cleaned['email'],
            password=cleaned['password1'], 
            userRole=cleaned['userRole'],
            userFirstName =cleaned['userFirstName'],
            userLastName=cleaned['userLastName'],
        )
    
        #if commit is true (basically if it's submitted), save the user    
        if commit:
            user.save()

        #returns the new user that was just created
        return user
    
