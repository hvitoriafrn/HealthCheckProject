from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


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