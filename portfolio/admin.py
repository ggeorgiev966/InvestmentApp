from django.contrib import admin
from .models import Stock, Bitcoin, Silver, InvestmentPortfolio


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'price', 'purchased_at', 'user',)
    search_fields = ('name', 'ticker')
    search_help_text = 'Search by stock name or ticker symbol.'
    list_filter = ('user', 'purchased_at')
    date_hierarchy = 'purchased_at'


@admin.register(Bitcoin)
class BitcoinAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'purchased_at', 'price', 'user',)
    list_filter = ('user', 'purchased_at')

@admin.register(Silver)
class SilverAdmin(admin.ModelAdmin):
    list_display = ('weight', 'purchased_at', 'price', 'user',)
    list_filter = ('user', 'purchased_at')

@admin.register(InvestmentPortfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)
    list_filter = ('created_at', 'user')
    ordering = ('created_at',)
