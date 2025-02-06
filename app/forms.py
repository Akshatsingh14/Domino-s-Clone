from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_img', 'phone','dob','age','gender']
    
    user_img = forms.ImageField(required=False)  # If image is optional
    phone = forms.IntegerField(required=False)  # If phone is optional
    dob = forms.DateField(required=False)  # If dob is optional
    age = forms.IntegerField(required=False)  # If age is optional