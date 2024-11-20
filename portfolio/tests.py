from django.test import TestCase
from django.contrib.auth.models import User
from .forms import RealEstateForm
from .models import UserProfile, InvestmentPortfolio, RealEstate, Stock, Bitcoin, Silver
from django.urls import reverse
from datetime import datetime

class RealEstateModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        self.realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            purchase_date="2023-11-20T12:00:00Z",
            user=user
        )

    def test_realestate_creation(self):
        self.assertEqual(self.realestate.property_name, "Test Property")
        self.assertEqual(self.realestate.purchase_price, 100000.00)
        self.assertEqual(str(self.realestate), "Test Property")

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_userprofile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(str(self.user_profile), 'testuser')

class InvestmentPortfolioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)

    def test_investmentportfolio_creation(self):
        self.assertEqual(self.portfolio.user, self.user_profile)
        self.assertEqual(str(self.portfolio), f'Portfolio of {self.user.username}')

class RealEstateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='12345')

    def test_realestate_create_view(self):
        response = self.client.get(reverse('add_realestate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/add_realestate.html')

        response = self.client.post(reverse('add_realestate'), {
            'property_name': 'Test Property',
            'purchase_price': 100000.00,
            'purchase_date': '2023-11-20T12:00:00Z',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RealEstate.objects.count(), 1)

    def test_realestate_update_view(self):
        realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            purchase_date="2023-11-20T12:00:00Z",
            user=self.user
        )
        response = self.client.get(reverse('edit_realestate', args=[realestate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/edit_realestate.html')

        response = self.client.post(reverse('edit_realestate', args=[realestate.id]), {
            'property_name': 'Updated Property',
            'purchase_price': 120000.00,
            'purchase_date': '2023-11-21T12:00:00Z',
        })
        self.assertEqual(response.status_code, 302)
        realestate.refresh_from_db()
        self.assertEqual(realestate.property_name, 'Updated Property')
        self.assertEqual(realestate.purchase_price, 120000.00)

    def test_realestate_delete_view(self):
        realestate = RealEstate.objects.create(
            property_name="Test Property",
            purchase_price=100000.00,
            purchase_date="2023-11-20T12:00:00Z",
            user=self.user
        )
        response = self.client.post(reverse('delete_realestate', args=[realestate.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RealEstate.objects.count(), 0)

class RealEstateFormTest(TestCase):
    def test_realestate_form_valid(self):
        form_data = {
            'property_name': 'Test Property',
            'purchase_price': 100000.00,
            'purchase_date': '2023-11-20T12:00:00Z',
        }
        form = RealEstateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_realestate_form_invalid(self):
        form_data = {
            'property_name': '',
            'purchase_price': '',
            'purchase_date': '',
        }
        form = RealEstateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

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
            'purchased_at': datetime.now(),
        })


        self.assertEqual(response.status_code, 302)


        bitcoin = Bitcoin.objects.first()
        self.assertEqual(bitcoin.quantity, 1.5)
        self.assertEqual(bitcoin.price, 60000.00)
        self.assertEqual(str(bitcoin), "1.50000000 BTC @ 60000.00 USD")


class StockViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user)


        self.portfolio = InvestmentPortfolio.objects.create(user=self.user_profile)


        self.client.login(username='testuser', password='12345')

    def test_stock_create_view(self):

        response = self.client.post(reverse('add_stock'), {
            'name': 'Test Stock',
            'ticker': 'TST',
            'price': 500.00,
            'purchased_at': datetime.now(),
        })


        self.assertEqual(response.status_code, 302)


        stock = Stock.objects.first()
        self.assertEqual(stock.name, 'Test Stock')
        self.assertEqual(stock.ticker, 'TST')
        self.assertEqual(stock.price, 500.00)
        self.assertEqual(str(stock), "Test Stock (TST) @ 500.00 USD")


class BitcoinModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')




        self.bitcoin = Bitcoin.objects.create(
            quantity=1.5,
            price=60000.00,
            purchased_at=datetime.now(),
            user=self.user
        )

    def test_bitcoin_creation(self):

        self.assertEqual(self.bitcoin.quantity, 1.5)
        self.assertEqual(self.bitcoin.price, 60000.00)
        self.assertEqual(str(self.bitcoin), "1.50000000 BTC @ 60000.00 USD")


class StockModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')


        self.stock = Stock.objects.create(
            name='Test Stock',
            ticker='TST',
            price=500.00,
            purchased_at=datetime.now(),
            user=self.user
        )

    def test_stock_creation(self):

        self.assertEqual(self.stock.name, 'Test Stock')
        self.assertEqual(self.stock.ticker, 'TST')
        self.assertEqual(self.stock.price, 500.00)
        self.assertEqual(str(self.stock), "Test Stock (TST) @ 500.00 USD")
