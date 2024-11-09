from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public Routes
    path('', views.home, name='home'),  # Homepage

    # Authentication Routes
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),  # Custom view for user registration

    # Private Routes - Accessible only to authenticated users
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),  # User Dashboard

    # Add Investment Routes
    path('add-stock/', views.StockCreateView.as_view(), name='add_stock'),
    path('add-bitcoin/', views.BitcoinCreateView.as_view(), name='add_bitcoin'),
    path('add-silver/', views.SilverCreateView.as_view(), name='add_silver'),
]