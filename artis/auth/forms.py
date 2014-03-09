from django import forms 

class LoginForm(forms.Form): 
    login = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
        