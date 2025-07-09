from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import URL

class URLModelTest(TestCase):
    def test_create_url(self):
        url = URL.objects.create(original_url="https://www.google.com", short_code="123456")
        self.assertEqual(url.original_url, "https://www.google.com")
        self.assertEqual(url.short_code, "123456")
        self.assertEqual(url.clicks, 0)

class URLShortenerViewTest(APITestCase):
    def test_shorten_new_url(self):
        url = reverse('url-shorten')
        data = {'original_url': 'https://www.example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(URL.objects.filter(original_url='https://www.example.com').exists())

    def test_shorten_existing_url(self):
        url_instance = URL.objects.create(original_url='https://www.example.com', short_code='existing')
        url = reverse('url-shorten')
        data = {'original_url': 'https://www.example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['short_code'], 'existing')

class URLRedirectViewTest(APITestCase):
    def setUp(self):
        self.url_instance = URL.objects.create(original_url='https://www.example.com', short_code='redirect')

    def test_redirect_valid_short_code(self):
        url = reverse('url-redirect', kwargs={'short_code': 'redirect'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, 'https://www.example.com')
        self.url_instance.refresh_from_db()
        self.assertEqual(self.url_instance.clicks, 1)

    def test_redirect_invalid_short_code(self):
        url = reverse('url-redirect', kwargs={'short_code': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)