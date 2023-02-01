from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from .models import MyUser

class LoginForm(ModelForm):
    class Meta:
        model = MyUser
        fields = [ 'username', 'password']

        help_texts = {
            'username' : _(''),
        }

        widgets = {
            "username": forms.TextInput(attrs= {"class" : "form-control"}),

            "password": forms.PasswordInput(attrs= {"class" : "form-control"})
        }



class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser

        fields = [ 'username' , 'first_name' , 'last_name' ,  'email' , 'date_of_birth', 'password1' , 'password2']


        help_texts = {
            'username' : None,
            'password1' :  None,
            'password2' :  None,
        }

        widgets = {
            "username": forms.TextInput(attrs= {"class" : "form-control"}),

            "first_name": forms.TextInput(attrs= {"class" : "form-control"}),

            "last_name": forms.TextInput(attrs= {"class" : "form-control"}),

            "email": forms.TextInput(attrs= {"class" : "form-control"}),

            "date_of_birth": forms.DateInput(attrs= {'type': 'date', "class" : "form-control"}),

            "password1": forms.TextInput(attrs= {"class" : "form-control"}),

            "password2": forms.TextInput(attrs= {"class" : "form-control"})
        }


    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user