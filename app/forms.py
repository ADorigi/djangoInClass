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
    comments = forms.CharField(widget=forms.Textarea)
    quantity = forms.IntegerField(initial = 1,validators=[ MinValueValidator(1)])


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'company',
                  'shipping_address', 'city', 'province']
