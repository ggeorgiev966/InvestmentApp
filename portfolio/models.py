from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

class Bitcoin(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Silver(models.Model):
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class InvestmentPortfolio(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, blank=True)
    bitcoins = models.ManyToManyField(Bitcoin, blank=True)
    silvers = models.ManyToManyField(Silver, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




