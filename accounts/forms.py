from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    age = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'Age is required for better recommendations '
        }
    )

    gender = forms.ChoiceField(
        choices=[
            ('', 'Select'),
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other')
        ],
        required=True,
        error_messages={
            'required': 'Please select your gender'
        }
    )

    city = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'City helps us find nearby doctors'
        }
    )

    phone = forms.CharField(
        max_length=15,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'age',
            'gender',
            'city',
            'phone'
        ]