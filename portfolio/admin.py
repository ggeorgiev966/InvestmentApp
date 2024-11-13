from django.contrib import admin
from .models import Stock, Bitcoin, Silver, InvestmentPortfolio

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'price', 'purchased_at', 'user')
    search_fields = ('name', 'ticker')
    ordering = ('price',)
    list_filter = ('user',)

@admin.register(Bitcoin)
class BitcoinAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'purchased_at', 'user')
    list_filter = ('user',)

@admin.register(Silver)
class SilverAdmin(admin.ModelAdmin):
    list_display = ('weight', 'purchased_at', 'user')
    list_filter = ('user',)

@admin.register(InvestmentPortfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)

