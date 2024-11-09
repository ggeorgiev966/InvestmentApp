from django import forms
from .models import Stock, Bitcoin, Silver

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'ticker', 'price']

class BitcoinForm(forms.ModelForm):
    class Meta:
        model = Bitcoin
        fields = ['quantity', 'purchased_at']

class SilverForm(forms.ModelForm):
    class Meta:
        model = Silver
        fields = ['weight', 'purchased_at']
