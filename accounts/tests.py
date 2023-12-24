from django.test import TestCase
from api.models import User


from django.contrib.auth import get_user_model, login

User = get_user_model()

# ログインできるか
# アカウントが作成できるか

class AccountTestCase(TestCase):
  def setUp(self):
    pass
  

  # 
  def test_pollを作成できるか(self):
    pass

  def test_投票ができるか(self):
    pass


