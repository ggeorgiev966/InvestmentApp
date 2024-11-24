from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import make_aware, now
from datetime import datetime

from .models import UserProfile, InvestmentPortfolio, RealEstate, Stock, Bitcoin, Silver
from .forms import RealEstateForm

# RealEstate Tests
class RealEstateModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            current_evaluation_price=120000.00,
            purchase_date=make_aware(datetime.now()),
            user=user
        )

    def test_realestate_creation(self):
        self.assertEqual(self.realestate.property_name, "Test Property")
        self.assertEqual(self.realestate.purchase_price, 100000.00)
        self.assertEqual(self.realestate.current_evaluation_price, 120000.00)
        self.assertEqual(str(self.realestate), "Test Property")


class RealEstateFormTest(TestCase):
    def test_realestate_form_valid(self):
        form_data = {
            'property_name': 'Test Property',
            'purchase_price': 100000.00,
            'current_evaluation_price': 120000.00,
            'purchase_date': now(),
        }
        form = RealEstateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_realestate_form_invalid(self):
        form_data = {
            'property_name': '',
            'purchase_price': '',
            'current_evaluation_price': '',
            'purchase_date': '',
        }
        form = RealEstateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class RealEstateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)
        self.client.login(username='testuser', password='12345')

    def test_realestate_create_view(self):
        response = self.client.post(reverse('add_realestate'), {
            'property_name': 'Test Property',
            'purchase_price': 100000.00,
            'current_evaluation_price': 120000.00,  # Include this field
            'purchase_date': '2023-11-20T12:00:00Z',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(RealEstate.objects.count(), 1)
        realestate = RealEstate.objects.first()
        self.assertEqual(realestate.current_evaluation_price, 120000.00)

    def test_realestate_update_view(self):
        realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            current_evaluation_price=120000.00,
            purchase_date=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.post(reverse('edit_realestate', args=[realestate.id]), {
            'property_name': 'Updated Property',
            'purchase_price': 120000.00,
            'current_evaluation_price': 150000.00,
            'purchase_date': '2023-11-20T12:00:00Z',
        })
        self.assertEqual(response.status_code, 302)
        realestate.refresh_from_db()
        self.assertEqual(realestate.property_name, 'Updated Property')
        self.assertEqual(realestate.current_evaluation_price, 150000.00)

    def test_realestate_delete_view(self):
        realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            purchase_date=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.post(reverse('delete_realestate', args=[realestate.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RealEstate.objects.count(), 0)

# Stock Tests
class StockModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.stock = Stock.objects.create(
            name="Test Stock",
            ticker="TST",
            price=500.00,
            purchased_at=make_aware(datetime.now()),
            user=user
        )

    def test_stock_creation(self):
        self.assertEqual(self.stock.name, "Test Stock")
        self.assertEqual(self.stock.ticker, "TST")
        self.assertEqual(self.stock.price, 500.00)
        self.assertEqual(str(self.stock), "Test Stock (TST) @ 500.00 USD")

class StockViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)
        self.client.login(username='testuser', password='12345')

    def test_stock_create_view(self):
        response = self.client.get(reverse('add_stock'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/add_stock.html')

        response = self.client.post(reverse('add_stock'), {
            'name': 'Test Stock',
            'ticker': 'TST',
            'price': 500.00,
            'quantity': 2,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)

    def test_stock_update_view(self):
        stock = Stock.objects.create(
            name="Test Stock",
            ticker="TST",
            price=500.00,
            quantity=2,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.get(reverse('edit_stock', args=[stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/edit_stock.html')

        response = self.client.post(reverse('edit_stock', args=[stock.id]), {
            'name': 'Updated Stock',
            'ticker': 'UST',
            'price': 600.00,
            'quantity': 2,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        stock.refresh_from_db()
        self.assertEqual(stock.name, 'Updated Stock')
        self.assertEqual(stock.ticker, 'UST')
        self.assertEqual(stock.price, 600.00)
        self.assertEqual(stock.quantity, 2)

    def test_stock_delete_view(self):
        stock = Stock.objects.create(
            name="Test Stock",
            ticker="TST",
            price=500.00,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.post(reverse('delete_stock', args=[stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 0)

# Bitcoin Tests
class BitcoinModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.bitcoin = Bitcoin.objects.create(
            quantity=1.5,
            price=60000.00,
            purchased_at=make_aware(datetime.now()),
            user=user
        )

    def test_bitcoin_creation(self):
        self.assertEqual(self.bitcoin.quantity, 1.5)
        self.assertEqual(self.bitcoin.price, 60000.00)
        self.assertEqual(str(self.bitcoin), "1.50000000 BTC @ 60000.00 USD")

class BitcoinViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)
        self.client.login(username='testuser', password='12345')

    def test_bitcoin_create_view(self):
        response = self.client.post(reverse('add_bitcoin'), {
            'quantity': 1.5,
            'price': 60000.00,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bitcoin.objects.count(), 1)

    def test_bitcoin_update_view(self):
        bitcoin = Bitcoin.objects.create(
            quantity=1.5,
            price=60000.00,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.get(reverse('edit_bitcoin', args=[bitcoin.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/edit_bitcoin.html')

        response = self.client.post(reverse('edit_bitcoin', args=[bitcoin.id]), {
            'quantity': 2.0,
            'price': 65000.00,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        bitcoin.refresh_from_db()
        self.assertEqual(bitcoin.quantity, 2.0)
        self.assertEqual(bitcoin.price, 65000.00)

    def test_bitcoin_delete_view(self):
        bitcoin = Bitcoin.objects.create(
            quantity=1.5,
            price=60000.00,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.post(reverse('delete_bitcoin', args=[bitcoin.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bitcoin.objects.count(), 0)

    # Silver Tests
class SilverModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.silver = Silver.objects.create(
            weight=50.0,
            price=1000.00,
            purchased_at=make_aware(datetime.now()),
            user=user
        )

    def test_silver_creation(self):
        self.assertEqual(self.silver.weight, 50.0)
        self.assertEqual(self.silver.price, 1000.00)
        self.assertEqual(str(self.silver), "50.00 oz @ 1000.00 USD")

class SilverViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)
        self.client.login(username='testuser', password='12345')

    def test_silver_create_view(self):
        response = self.client.get(reverse('add_silver'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/add_silver.html')

        response = self.client.post(reverse('add_silver'), {
            'weight': 50.0,
            'price': 1000.00,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Silver.objects.count(), 1)

    def test_silver_update_view(self):
        silver = Silver.objects.create(
            weight=50.0,
            price=1000.00,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.get(reverse('edit_silver', args=[silver.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/edit_silver.html')

        response = self.client.post(reverse('edit_silver', args=[silver.id]), {
            'weight': 60.0,
            'price': 1100.00,
            'purchased_at': make_aware(datetime.now()),
        })
        self.assertEqual(response.status_code, 302)
        silver.refresh_from_db()
        self.assertEqual(silver.weight, 60.0)
        self.assertEqual(silver.price, 1100.00)

    def test_silver_delete_view(self):
        silver = Silver.objects.create(
            weight=50.0,
            price=1000.00,
            purchased_at=make_aware(datetime.now()),
            user=self.user
        )
        response = self.client.post(reverse('delete_silver', args=[silver.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Silver.objects.count(), 0)

