import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TestUserView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'testuser'
        cls.password = 'testpassword'
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_profile_detail_authorized(self):
        url = reverse('accounts:profile_view')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['username'])
        self.assertEqual(json.loads(response.content), {'email': None, 'profile_image': None, 'username': 'testuser'})

    def test_profile_detail_unauthorized(self):
        url = reverse('accounts:profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_profile_update_authorized(self):
        url = reverse('accounts:profile_view')
        data = {
            'username': 'testuser'
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_unauthorized(self):
        url = reverse('accounts:profile_view')
        data = {
            'username': 'testuser'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login(self):
        url = reverse('accounts:login')
        data = {
            'username': self.username,
            'password': self.password
        }
        
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.failUnless(response.data['access'])