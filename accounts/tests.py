from django.test import TestCase
from api.models import User
from django.urls import reverse

from django.contrib.auth import get_user_model, login

User = get_user_model()

# ログインできるか
# アカウントが作成できるか

class AccountTestCase(TestCase):
  def setUp(self):
    self.user_data = {
      'email': 'test@example.com',
      'password1': 'jfaljfiwehfpuaheuifh',
      'password2': "jfaljfiwehfpuaheuifh",
    }
  
  def test_signup(self):
    """アカウント作成のテスト"""
    print(self.user_data)
    response = self.client.post(reverse('signup'), self.user_data)
    self.assertEqual(response.status_code, 200)
    # ユーザーが作成されたかどうかを確認
    self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())


