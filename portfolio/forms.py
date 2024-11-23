from django import forms
from .models import Stock, Bitcoin, Silver, RealEstate


class StockForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Stock
        fields = ['name', 'ticker', 'price', 'purchased_at']

    price = forms.DecimalField(label="Price ($)", max_digits=10, decimal_places=2)


class BitcoinForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    price = forms.DecimalField(label="Price ($)", max_digits=10, decimal_places=2)

    class Meta:
        model = Bitcoin
        fields = ['quantity', 'price', 'purchased_at']



class SilverForm(forms.ModelForm):
    purchased_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    price = forms.DecimalField(label="Price ($)", max_digits=10, decimal_places=2)
    weight = forms.DecimalField(label="Weight (oz)", max_digits=5, decimal_places=2)

    class Meta:
        model = Silver
        fields = ['weight', 'price', 'purchased_at']


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


class RealEstateForm(forms.ModelForm):
    purchase_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    purchase_price = forms.DecimalField(label="Price ($)", max_digits=10, decimal_places=2)
    current_evaluation_price = forms.DecimalField(label="Current Evaluation Price ($)", max_digits=10, decimal_places=2)

    class Meta:
        model = RealEstate
        fields = ['property_name', 'purchase_price', 'purchase_date', 'current_evaluation_price']

