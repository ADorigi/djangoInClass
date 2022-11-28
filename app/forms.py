from django import forms
from django.core.validators import MinValueValidator

from app.models import Order, Client, Category


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {
            'client': forms.RadioSelect
        }
        labels = {
            "client": "Client Name",
            "num_units": "Quantity"
        }


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices= ((1,'Yes'), (0,'No')))
    quantity = forms.IntegerField(initial = 1,validators=[ MinValueValidator(1)], 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'company',
                  'shipping_address', 'city', 'province', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),

        }


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
