from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}), label="Confirm Password")
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2'
        ]

    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if data is None or data == "" or data == " ":
            raise ValidationError("First name cannot be empty!")
        
        if len(data) < 5:
            raise ValidationError("First name must be at least 5 characters!")
        return data 
    
    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        if data is None or data == "" or data == " ":
            raise ValidationError("Last name cannot be empty!")
        
        if len(data) < 5:
            raise ValidationError("Last name must be at least 5 characters!")
        return data 
    
    def clean_email(self):
        data = self.cleaned_data.get('email')
        is_exist = User.objects.filter(email=data).exists()
        if is_exist:
            raise ValidationError("Email already exist!")

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        #check for password length at least 8 characters.
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters!")
        return password
    
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        #check for password and password2 is match.
        if password != password2:
            raise ValidationError("Confirm password must be same!")
        
        return password2