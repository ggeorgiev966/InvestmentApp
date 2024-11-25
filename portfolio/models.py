from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Bitcoin(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity:.8f} BTC @ {self.price:.2f} USD"

class Silver(models.Model):
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.weight:.2f} oz @ {self.price:.2f} USD"

class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.ticker}) @ {self.price:.2f} USD"

class InvestmentPortfolio(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, blank=True)
    bitcoins = models.ManyToManyField(Bitcoin, blank=True)
    silvers = models.ManyToManyField(Silver, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio of {self.user.user.username}"


class RealEstate(models.Model):
    property_name = models.CharField(max_length=100)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_evaluation_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.property_name

class LastAvailablePrice(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=8)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol}: {self.price}"
