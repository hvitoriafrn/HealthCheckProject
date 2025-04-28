from django import forms
from .models import CustomUser

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['userFirstName', 'userLastName', 'email', 'userTeam', 'userRole']
        labels = {
            'userFirstName': 'First name',
            'userLastName': 'Last name',
            'email': 'Email address',
            'userTeam': 'Team',
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
        user.userTeam = self.cleaned_data['userTeam']
        
        # For disabled fields, use initial values
        user.userRole = self.initial.get('userRole') 
        
        if commit:
            user.save()
        return user

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['userFirstName', 'userLastName', 'email', 'userTeam', 'userRole']
        labels = {
            'userFirstName': 'First name',
            'userLastName': 'Last name',
            'email': 'Email address',
            'userTeam': 'Team',
            'userRole': 'Role'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        cleaned = self.cleaned_data
        user = CustomUser.objects.create_user(
            email=cleaned['email'],
            password=cleaned['password1'],
            role=cleaned['userRole'],
            userFirstName=cleaned['userFirstName'],
            userLastName=cleaned['userLastName'],
            userTeam=cleaned.get('userTeam')
        )
        if commit:
            user.save()
        return user