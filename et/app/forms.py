from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
 
 
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget= forms.TextInput(attrs={'placeholder':'Email'}))
    username = forms.CharField(max_length = 20,widget= forms.TextInput(attrs={'placeholder':'Username'}))
    password1= forms.CharField(max_length = 20,widget= forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2= forms.CharField(max_length = 20,widget= forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))



    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def check_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if(password1 != password2):
            raise forms.ValidationError("Passwords don't match")
        return password2
    
class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(max_length = 20,widget= forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(max_length = 20,widget= forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def check_password(self):
        password = self.cleaned_data.get('password')
        return password