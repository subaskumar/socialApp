from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_pass(value):
    if len(value) < 4:
        raise ValidationError('password must be contain 5 character')

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),validators=[validate_pass])
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name','email']