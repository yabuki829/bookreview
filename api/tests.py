from django.test import TestCase
from .models import Book
from utils.book_service import BookService


# 本の検索
class BookTestCase(TestCase):
  def setUp(self):
    pass
  
  def test_fetch_book_from_GoogleBooksAPI(self):
    """Google Books API から本を取得できるかのテスト"""
    isnb = "9784798068169"

    servise = BookService() 
    response = servise.get_book_with_isbn(isnb)
    self.assertIsNotNone(response)







