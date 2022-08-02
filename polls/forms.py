from cProfile import label
from django import forms
from django.core.validators import MinLengthValidator
class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    Email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(), validators=[MinLengthValidator(limit_value=8, message='short password')])
    first_name = forms.CharField(label='First_name' , max_length=200)
    last_name = forms.CharField(label='Last_name')