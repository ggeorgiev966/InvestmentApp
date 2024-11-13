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
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Bitcoin
        fields = ['quantity', 'price', 'purchased_at']


class SilverForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Silver
        fields = ['weight', 'price', 'purchased_at']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
