from django.urls import path

from . import views
from .views import home, PortfolioView, StockCreateView, BitcoinCreateView, SilverCreateView, register, \
    bitcoin_price_view, StockUpdateView, BitcoinUpdateView, SilverUpdateView, DeleteBitcoinView, DeleteSilverView, \
    DeleteStockView, ConfirmDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('register/', register, name='register'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('add-stock/', StockCreateView.as_view(), name='add_stock'),
    path('add-bitcoin/', BitcoinCreateView.as_view(), name='add_bitcoin'),
    path('add-silver/', SilverCreateView.as_view(), name='add_silver'),
    path('api/bitcoin-price/', bitcoin_price_view, name='bitcoin_price_view'),
    path('api/silver-price/', SilverCreateView.as_view(), name='silver_price_view'),
    path('edit-stock/<int:pk>/', StockUpdateView.as_view(), name='edit_stock'),
    path('edit-bitcoin/<int:pk>/', BitcoinUpdateView.as_view(), name='edit_bitcoin'),
    path('edit-silver/<int:pk>/', SilverUpdateView.as_view(), name='edit_silver'),
    path('delete_bitcoin/<int:pk>/', DeleteBitcoinView.as_view(), name='delete_bitcoin'),
    path('delete_stock/<int:pk>/', DeleteStockView.as_view(), name='delete_stock'),
    path('delete_silver/<int:pk>/', DeleteSilverView.as_view(), name='delete_silver'),
    path('confirm_delete/<str:model_name>/<int:pk>/', ConfirmDeleteView.as_view(), name='confirm_delete'),
]

