from django import forms
from .models import Vegetable, Transaction

class AddVegForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ['name', 'description', 'price', 'img']

class NewTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['tran_type', 'details']