from django.urls import path

from . import views
from .views import home, PortfolioView, StockCreateView, BitcoinCreateView, SilverCreateView, register, \
    bitcoin_price_view, StockUpdateView, BitcoinUpdateView, SilverUpdateView, DeleteBitcoinView, DeleteSilverView, \
    DeleteStockView, ConfirmDeleteView, silver_price_view, stock_price_view, RealEstateCreateView, RealEstateUpdateView, \
    DeleteRealEstateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('register/', register, name='register'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('add-stock/', StockCreateView.as_view(), name='add_stock'),
    path('add-bitcoin/', BitcoinCreateView.as_view(), name='add_bitcoin'),
    path('add-silver/', SilverCreateView.as_view(), name='add_silver'),
    path('add_realestate/', RealEstateCreateView.as_view(), name='add_realestate'),
    path('api/bitcoin-price/', bitcoin_price_view, name='bitcoin_price_view'),
    path('api/silver-price/', silver_price_view, name='silver_price_view'),
    path('api/stock-price/<str:symbol>/', stock_price_view, name='stock_price_view'),
    path('edit-stock/<int:pk>/', StockUpdateView.as_view(), name='edit_stock'),
    path('edit-bitcoin/<int:pk>/', BitcoinUpdateView.as_view(), name='edit_bitcoin'),
    path('edit-silver/<int:pk>/', SilverUpdateView.as_view(), name='edit_silver'),
    path('edit_realestate/<int:pk>/', RealEstateUpdateView.as_view(), name='edit_realestate'),
    path('delete_bitcoin/<int:pk>/', DeleteBitcoinView.as_view(), name='delete_bitcoin'),
    path('delete_stock/<int:pk>/', DeleteStockView.as_view(), name='delete_stock'),
    path('delete_silver/<int:pk>/', DeleteSilverView.as_view(), name='delete_silver'),
    path('delete_realestate/<int:pk>/', DeleteRealEstateView.as_view(), name='delete_realestate'),
    path('confirm_delete/<str:model_name>/<int:pk>/', ConfirmDeleteView.as_view(), name='confirm_delete'),
]

