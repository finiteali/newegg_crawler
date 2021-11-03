from django.test import TestCase, Client
from . import views
from unittest import mock
from unittest.mock import patch
from django.conf import settings
import os
import json


# def side_effect(*args, **kwargs):
#     m = mock.MagicMock()
#     m.content.return_value = ''
#     # m.__len__.return_value = 100
#     return m


# class MyIpMockResponse:
#     def json(self):
#         return {"ip": "1.1.1.1"}


# class TestMyIpAPI(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
#
#     @patch('crawler.service.get_my_ip')
#     def test_fetch_my_ip(self, mock_request):
#         expected_value = {"ip": "1.1.1.1"}
#         mock_request.return_value = {"ip": "1.1.1.1"}
#         result = self.client.get('/myip')
#         self.assertEqual(result.json(), expected_value)


# class TestProduct(TestCase):
#     @patch('requests.get')
#     def test_get(self, mock_request):
#         # print(mock_request)
#         mock_request.return_value = FakeResponse()
#         print(self.client.get('/product/N82E16832233101').json())


class FakeResponse:
    def __init__(self, filename):
        with open(os.path.join(settings.BASE_DIR, 'crawler', 'snapshots', f'{filename}.html'), 'r') as f:
            self.content = f.read()


class ReadExpect:
    def __init__(self, filename):
        with open(os.path.join(settings.BASE_DIR, 'crawler', 'snapshots', f'{filename}.json')) as json_file:
            self.content = json.load(json_file)


class TestGetProduct(TestCase):
    code = 'N82E16832233101'

    @patch('requests.get')
    def setUp(self, mock_request):
        mock_request.return_value = FakeResponse(filename=self.code)
        self.response = self.client.get(f'/product/{self.code}')
        self.json_response = self.response.json()
        self.expect = ReadExpect(filename=self.code).content

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_title(self):
        expect_title = self.expect['title']
        real_title = self.json_response['title']
        self.assertEqual(expect_title, real_title)

    def test_brand(self):
        expect_brand = self.expect['brand']
        real_brand = self.json_response['brand']
        self.assertEqual(expect_brand, real_brand)

    def test_main_price(self):
        expect_price = self.expect['main_price']
        real_price = self.json_response['main_price']
        self.assertEqual(expect_price, real_price)

    def test_deal_price(self):
        expect_price = self.expect['deal_price']
        real_price = self.json_response['deal_price']
        self.assertEqual(expect_price, real_price)

    def test_seller(self):
        expect_seller = self.expect['seller']
        real_seller = self.json_response['seller']
        self.assertEqual(expect_seller, real_seller)

    def test_count(self):
        expect_count = self.expect['count']
        real_count = self.json_response['count']
        self.assertEqual(expect_count, real_count)

    def test_stars(self):
        expect_stars = self.expect['stars']
        real_stars = self.json_response['stars']
        self.assertEqual(expect_stars, real_stars)

    def test_features(self):
        expect_features = self.expect['features']
        real_features = self.json_response['features']
        self.assertEqual(expect_features, real_features)


class TestGetProduct2(TestGetProduct):
    code = 'N82E16832233101'
