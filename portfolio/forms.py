from django import forms
from .models import Stock, Bitcoin, Silver


class StockForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Stock
        fields = ['name', 'ticker', 'price', 'purchased_at']


class BitcoinForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    price = forms.DecimalField(max_digits=10, decimal_places=2)  # Add the price field

    class Meta:
        model = Bitcoin
        fields = ['quantity', 'price', 'purchased_at']  # Include the price field


class SilverForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    price = forms.DecimalField(max_digits=10, decimal_places=2)  # Add the price field

    class Meta:
        model = Silver
        fields = ['weight', 'price', 'purchased_at']  # Include the price field
