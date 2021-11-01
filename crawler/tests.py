from django.test import TestCase, Client
from . import views
from unittest import mock


def side_effect(*args, **kwargs):
    m = mock.MagicMock()
    m.content.return_value = ''
    # m.__len__.return_value = 100
    return m


class TestGetProduct(TestCase):
    @mock.patch('requests.request', return_value=side_effect())
    def setUp(self, l):
        c = Client()
        self.response = c.get('/product/N82E16832233101')
        self.json_response = self.response.json()

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_title(self):
        expect_title = 'RESIDENT EVIL 3 [Online Game Code]'
        real_title = self.json_response['title']
        self.assertEqual(expect_title, real_title)

    def test_brand(self):
        expect_brand = 'Capcom'
        real_brand = self.json_response['brand']
        self.assertEqual(expect_brand, real_brand)

    def test_main_price(self):
        expect_price = 59.99
        real_price = self.json_response['main_price']
        self.assertEqual(expect_price, real_price)

    def test_deal_price(self):
        expect_price = 17.79
        real_price = self.json_response['deal_price']
        self.assertEqual(expect_price, real_price)

    def test_seller(self):
        expect_seller = 'Newegg'
        real_seller = self.json_response['seller']
        self.assertEqual(expect_seller, real_seller)

    def test_count(self):
        expect_count = 18
        real_count = self.json_response['count']
        self.assertEqual(expect_count, real_count)

    def test_stars(self):
        expect_stars = 5
        real_stars = self.json_response['stars']
        self.assertEqual(expect_stars, real_stars)

    def test_features(self):
        expect_features = ['Capcom', 'ESRB Rating M - Mature', 'Genre Action Adventure', 'DRM Steam']
        real_features = self.json_response['features']
        self.assertEqual(expect_features, real_features)
