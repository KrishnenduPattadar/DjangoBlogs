from django import forms
from django.contrib.auth.models import User
from .models import Profile, BlogPost

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['image', 'description']
