from django.urls import reverse_lazy
from django.views.generic import UpdateView
from InvestmentApp import settings
from .apis import get_silver_price, get_bitcoin_price, get_stock_price
from .forms import StockForm, BitcoinForm, SilverForm, ContactForm, RealEstateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InvestmentPortfolio, UserProfile, Silver, Stock, Bitcoin, RealEstate
from django.core.mail import EmailMessage
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class PortfolioView(View):
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
        total_real_estate_purchase_price = sum(float(realestate.purchase_price) for realestate in RealEstate.objects.filter(user=request.user))
        total_real_estate_evaluation_price = sum(float(realestate.current_evaluation_price) for realestate in RealEstate.objects.filter(user=request.user) if realestate.current_evaluation_price)

        # Get current Bitcoin and Silver prices
        current_bitcoin_price, bitcoin_price_message = get_bitcoin_price()
        if current_bitcoin_price is None:
            current_bitcoin_price = 0.0  # Assign a default value if price is None
        else:
            current_bitcoin_price = float(current_bitcoin_price.replace(',', ''))

        current_silver_price, silver_price_message = get_silver_price()
        if current_silver_price is None:
            current_silver_price = 0.0  # Assign a default value if price is None

        # Calculate Bitcoin and Silver profit/loss
        bitcoin_profit_loss = (current_bitcoin_price - avg_bitcoin_price) * total_bitcoin_quantity
        silver_profit_loss = (current_silver_price - avg_silver_price) * total_silver_weight

        # Calculate Bitcoin and Silver profit/loss percentage
        bitcoin_profit_percentage = (bitcoin_profit_loss / total_bitcoin_price) * 100 if total_bitcoin_price else 0.0
        silver_profit_percentage = (silver_profit_loss / total_silver_price) * 100 if total_silver_price else 0.0

        # Calculate Real Estate profit/loss
        real_estate_profit_loss = total_real_estate_evaluation_price - total_real_estate_purchase_price
        real_estate_profit_percentage = (real_estate_profit_loss / total_real_estate_purchase_price) * 100 if total_real_estate_purchase_price else 0.0

        # Calculate total investment cost
        total_investment_cost = total_bitcoin_price + total_silver_price + total_spent_on_stocks + total_real_estate_purchase_price

        # Calculate total profit/loss
        total_profit_loss = bitcoin_profit_loss + silver_profit_loss + real_estate_profit_loss
        total_profit_percentage = (total_profit_loss / total_investment_cost) * 100 if total_investment_cost else 0.0

        context = {
            'portfolio': portfolio,
            'total_bitcoin_quantity': total_bitcoin_quantity,
            'avg_bitcoin_price': avg_bitcoin_price,
            'total_bitcoin_price': total_bitcoin_price,
            'total_silver_weight': total_silver_weight,
            'avg_silver_price': avg_silver_price,
            'total_silver_price': total_silver_price,
            'total_spent_on_stocks': total_spent_on_stocks,
            'total_real_estate_purchase_price': total_real_estate_purchase_price,
            'total_real_estate_evaluation_price': total_real_estate_evaluation_price,
            'real_estate_profit_loss': real_estate_profit_loss,
            'real_estate_profit_percentage': real_estate_profit_percentage,
            'current_bitcoin_price': current_bitcoin_price,
            'current_silver_price': current_silver_price,
            'total_investment_cost': total_investment_cost,
            'bitcoin_profit_loss': bitcoin_profit_loss,
            'silver_profit_loss': silver_profit_loss,
            'bitcoin_profit_percentage': bitcoin_profit_percentage,
            'silver_profit_percentage': silver_profit_percentage,
            'total_profit_loss': total_profit_loss,
            'total_profit_percentage': total_profit_percentage,
            'stocks': portfolio.stocks.all(),
            'bitcoins': portfolio.bitcoins.all(),
            'silvers': portfolio.silvers.all(),
            'realestates': RealEstate.objects.filter(user=request.user),
            'bitcoin_price_message': bitcoin_price_message,
            'silver_price_message': silver_price_message,
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
        'realestate': RealEstate
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

@method_decorator(login_required, name='dispatch')
class RealEstateCreateView(View):
    def get(self, request):
        form = RealEstateForm()
        return render(request, 'portfolio/add_realestate.html', {'form': form})

    def post(self, request):
        form = RealEstateForm(request.POST)
        if form.is_valid():
            realestate = form.save(commit=False)
            realestate.user = request.user
            realestate.save()
            return redirect('portfolio')
        return render(request, 'portfolio/add_realestate.html', {'form': form})

class RealEstateUpdateView(LoginRequiredMixin, UpdateView):
    model = RealEstate
    form_class = RealEstateForm
    template_name = 'portfolio/edit_realestate.html'
    success_url = reverse_lazy('portfolio')

class DeleteRealEstateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        realestate = get_object_or_404(RealEstate, pk=pk)
        realestate.delete()
        return redirect('portfolio')

def bitcoin_price_view(request):
    current_bitcoin_price, message = get_bitcoin_price()
    if message:
        return JsonResponse({'current_bitcoin_price': current_bitcoin_price, 'error': message})
    return JsonResponse({'current_bitcoin_price': current_bitcoin_price})


def silver_price_view(request):
    current_silver_price, message = get_silver_price()
    if message:
        return JsonResponse({'current_silver_price': current_silver_price, 'error': message})
    return JsonResponse({'current_silver_price': current_silver_price})

def stock_price_view(request, symbol):
    result = get_stock_price(symbol)
    print(f"Fetched price for {symbol}: {result['current_stock_price']}, Message: {result['error']}")  # Debug print
    return JsonResponse(result)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            user_email = form.cleaned_data['email']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['g.georgiev96@abv.bg']


            full_message = f"From: {user_email}\n\nMessage:\n{message}"

            email = EmailMessage(
                subject,
                full_message,
                from_email,
                recipient_list,
                reply_to=[user_email]
            )
            email.send(fail_silently=False)
            return redirect('thank_you')
    else:
        form = ContactForm()
    return render(request, 'portfolio/contact.html', {'form': form})


def thank_you(request):
    return render(request, 'portfolio/thank_you.html')





