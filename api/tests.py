from django.test import TestCase
from .models import Book
from .views import search


# 本の検索
class BookTestCase(TestCase):
  def setUp(self):
    pass
  
  def test_fetch_book_from_GoogleBooksAPI(self):
    """Google Books API から本を取得できるかのテスト"""
    isnb = "9784798068169"
    response = search.get_books_from_Google_Books_API(isnb)
    self.assertIsNotNone(response)







