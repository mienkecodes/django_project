# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# create new user - sign up
class CustomUserCreationForm(UserCreationForm):
    class Meta:    #CHANGES WE ARE MAKING      
        model = CustomUser        
        fields = ['username', 'email']
    
    class CustomUserChangeForm(UserChangeForm):
        class Meta:        
            model = CustomUser        
            fields = ['username', 'email']
            
            
            

            