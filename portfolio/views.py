from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import StockForm, BitcoinForm, SilverForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InvestmentPortfolio, UserProfile, Silver, Stock, Bitcoin
import requests

class PortfolioView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        portfolio, created = InvestmentPortfolio.objects.get_or_create(user=user_profile)

        # Calculate totals and averages
        total_bitcoin_quantity = sum(float(bitcoin.quantity) for bitcoin in portfolio.bitcoins.all())
        total_bitcoin_price = sum(float(bitcoin.quantity) * float(bitcoin.price) for bitcoin in portfolio.bitcoins.all())
        avg_bitcoin_price = total_bitcoin_price / total_bitcoin_quantity if total_bitcoin_quantity else 0.0

        total_silver_weight = sum(float(silver.weight) for silver in portfolio.silvers.all())
        total_silver_price = sum(float(silver.weight) * float(silver.price) for silver in portfolio.silvers.all())
        avg_silver_price = total_silver_price / total_silver_weight if total_silver_weight else 0.0

        total_spent_on_stocks = sum(float(stock.price) for stock in portfolio.stocks.all())

        # Get current Bitcoin and Silver prices
        current_bitcoin_price = get_bitcoin_price()
        if current_bitcoin_price is None:
            current_bitcoin_price = 0.0  # Assign a default value if price is None
        else:
            current_bitcoin_price = float(current_bitcoin_price.replace(',', ''))

        current_silver_price = get_silver_price()
        if current_silver_price is None:
            current_silver_price = 0.0  # Assign a default value if price is None

        # Calculate Bitcoin and Silver profit/loss
        bitcoin_profit_loss = (current_bitcoin_price - avg_bitcoin_price) * total_bitcoin_quantity
        silver_profit_loss = (current_silver_price - avg_silver_price) * total_silver_weight

        # Calculate total investment cost
        total_investment_cost = total_bitcoin_price + total_silver_price + total_spent_on_stocks

        # Calculate total profit/loss
        total_profit_loss = bitcoin_profit_loss + silver_profit_loss

        context = {
            'portfolio': portfolio,
            'total_bitcoin_quantity': total_bitcoin_quantity,
            'avg_bitcoin_price': avg_bitcoin_price,
            'total_bitcoin_price': total_bitcoin_price,
            'total_silver_weight': total_silver_weight,
            'avg_silver_price': avg_silver_price,
            'total_silver_price': total_silver_price,
            'total_spent_on_stocks': total_spent_on_stocks,
            'current_bitcoin_price': current_bitcoin_price,
            'current_silver_price': current_silver_price,
            'total_investment_cost': total_investment_cost,
            'bitcoin_profit_loss': bitcoin_profit_loss,
            'silver_profit_loss': silver_profit_loss,
            'total_profit_loss': total_profit_loss,
            'stocks': portfolio.stocks.all(),
            'bitcoins': portfolio.bitcoins.all(),
            'silvers': portfolio.silvers.all()
        }

        return render(request, 'portfolio/dashboard.html', context)


class StockCreateView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = StockForm()
        return render(request, 'portfolio/add_stock.html', {'form': form})

    def post(self, request):
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user  # Assign the authenticated User instance
            stock.save()
            portfolio = InvestmentPortfolio.objects.get(user=request.user.userprofile)
            portfolio.stocks.add(stock)
            portfolio.save()
            return redirect('portfolio')
        return render(request, 'portfolio/add_stock.html', {'form': form})

class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'portfolio/edit_stock.html'
    success_url = reverse_lazy('portfolio')

def home(request):
    return render(request, 'portfolio/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            InvestmentPortfolio.objects.create(user=user_profile)
            login(request, user)
            return redirect('portfolio')
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class BitcoinCreateView(View):
    def get(self, request):
        form = BitcoinForm()
        return render(request, 'portfolio/add_bitcoin.html', {'form': form})

    def post(self, request):
        form = BitcoinForm(request.POST)
        if form.is_valid():
            bitcoin = form.save(commit=False)
            bitcoin.user = request.user
            bitcoin.save()
            portfolio = InvestmentPortfolio.objects.get(user=request.user.userprofile)
            portfolio.bitcoins.add(bitcoin)
            return redirect('portfolio')
        return render(request, 'portfolio/add_bitcoin.html', {'form': form})

class BitcoinUpdateView(LoginRequiredMixin, UpdateView):
    model = Bitcoin
    form_class = BitcoinForm
    template_name = 'portfolio/edit_bitcoin.html'
    success_url = reverse_lazy('portfolio')

class DeleteBitcoinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        bitcoin = get_object_or_404(Bitcoin, pk=pk)
        bitcoin.delete()
        return redirect('portfolio')


@method_decorator(login_required, name='dispatch')
class SilverCreateView(View):
    def get(self, request):
        form = SilverForm()
        return render(request, 'portfolio/add_silver.html', {'form': form})

    def post(self, request):
        form = SilverForm(request.POST)
        if form.is_valid():
            silver = form.save(commit=False)
            silver.user = request.user
            silver.save()
            portfolio = InvestmentPortfolio.objects.get(user=request.user.userprofile)
            portfolio.silvers.add(silver)
            return redirect('portfolio')
        return render(request, 'portfolio/add_silver.html', {'form': form})

class SilverUpdateView(LoginRequiredMixin, UpdateView):
    model = Silver
    form_class = SilverForm
    template_name = 'portfolio/edit_silver.html'
    success_url = reverse_lazy('portfolio')


class DeleteStockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()
        return redirect('portfolio')

class DeleteSilverView(LoginRequiredMixin, View):
    def post(self, request, pk):
        silver = get_object_or_404(Silver, pk=pk)
        silver.delete()
        return redirect('portfolio')

class ConfirmDeleteView(LoginRequiredMixin, View):
    model_map = {
        'stock': Stock,
        'bitcoin': Bitcoin,
        'silver': Silver,
    }

    def get(self, request, model_name, pk):
        model = self.model_map.get(model_name)
        if not model:
            return redirect('portfolio')  # Or handle the error appropriately
        item = get_object_or_404(model, pk=pk)
        return render(request, 'portfolio/confirm_delete.html', {'item': item, 'model_name': model_name})

    def post(self, request, model_name, pk):
        model = self.model_map.get(model_name)
        if not model:
            return redirect('portfolio')  # Or handle the error appropriately
        item = get_object_or_404(model, pk=pk)
        item.delete()
        return redirect('portfolio')



def get_bitcoin_price():
    try:
        url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
        response = requests.get(url)
        data = response.json()
        return data['bpi']['USD']['rate']
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

from django.http import JsonResponse

def bitcoin_price_view(request):
    current_bitcoin_price = get_bitcoin_price()
    return JsonResponse({'current_bitcoin_price': current_bitcoin_price})

def get_silver_price():
    api_key = "goldapi-btin6sm3artlym-io"
    symbol = "XAG"
    curr = "USD"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['price']
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        return None


def silver_price_view(request):
    current_silver_price = get_silver_price()
    return JsonResponse({'current_silver_price': current_silver_price})




