from django import forms
from .models import Order


class OrderForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    package_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_package_id'}))
    contact_method = forms.ChoiceField(
        choices=Order.CONTACT_CHOICES,
        initial=Order.CONTACT_TELEGRAM,
        widget=forms.RadioSelect,
        label='How should we contact you?',
    )
