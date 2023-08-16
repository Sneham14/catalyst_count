from django import forms
from allauth.account.forms import SignupForm
from .models import UserModel, CompanyDataModel

class UserRegistrationForm(SignupForm):
    full_name = forms.CharField(max_length=120, label='Full Name')

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'full_name', 'password1', 'password2')

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = CompanyDataModel
        fields = '__all__'
        widgets = {
            'industry': forms.Select(attrs={'class': 'form-control'}),
        }

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username','is_active', )

