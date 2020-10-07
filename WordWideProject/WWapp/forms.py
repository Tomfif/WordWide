from django import forms
from django.contrib.auth.models import User

from WWapp.models import Story


class AddUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='first_name', max_length=100)
    last_name = forms.CharField(label='last_name', max_length=100)
    mail = forms.EmailField(label='mail', max_length=100,)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords are not the same!')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).exists()
            if user:
                raise forms.ValidationError('Login exists')
        return username


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class StoryForm(forms.ModelForm):
    title =  forms.CharField(disabled=True)
    author =  forms.CharField(disabled=True)
    genre =  forms.CharField(disabled=True)
    hero =  forms.CharField(disabled=True)
    world =  forms.CharField(disabled=True)
    class Meta:
        model = Story
        fields = ['title', 'author', 'genre', 'hero', 'world', 'content']