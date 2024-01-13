

"""
1. get_book_with_isbn(isbn) 
    isbnを使用して本をを取得する

2. get_book_with_title(title) 
    titleを使用して本をを取得する

3. format_isbn(isbn) 
    isbnをXXXX-X-XXXX-XXXX-X.の形に変換する  

4. is_isbn13(str)
    文字列がisbnかどうかを判別 
    13と書かれているが 10も通すので isbnかどうかを判別するために使う

5. convert_isbn10_to_isbn13()
    isbn10をisbn13に変換する 
    元々isbn13の場合はそのままisbn13を返す

"""

import re
import requests
from datetime import datetime

# 画像系
from django.core.files.base import ContentFile
from io import BytesIO

from api.models import Book,Category

class BookService():
  def get_books_with_title(self,title):
    books = Book.objects.filter(title__icontains=title)
    return books

  def get_book_with_isbn(self,isbn):
    print("isbnを使用して検索します")
    # もし既に登録済みであれば本を返す
    isbn13 = self.convert_isbn10_to_isbn13(isbn)
    print("isbn:",isbn13)
    books = Book.objects.filter(isbn=isbn13)
    if  books.exists():
      return books

    # 登録済みでなければ本を取得する    
    response = self.__get_books_from_Google_Books_API(isbn13)
    if response.status_code == 200:
      result = response.json()
      items = result.get('items', [])

      if items:
        book_info = items[0]['volumeInfo']

        # 画像処理
        image_url = book_info.get('imageLinks', {}).get('thumbnail')
        print("画像だよ",image_url)
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # BytesIOを使用して一時ファイルを作成する
                image_temp = BytesIO(image_response.content)
 

        published_date = book_info.get('publishedDate', '')
        # 日付を修正
        published_at = self.__parse_partial_date(published_date)
        category_name_en = book_info.get('categories', [''])[0]
        # カテゴリを作成
        category, created = Category.objects.get_or_create(name_en=category_name_en)
        title = book_info.get('title', '')

        book = Book(
          isbn=isbn13,
            title=title,
            subTitle=book_info.get("subtitle",""),
            author=book_info.get('authors', [''])[0],  # 代表者一名のみ取得
            description=book_info.get('description', ''),
            published_at=published_at,
            category=category
        )
        if image_url:
          book.image.save(f"{book.id}.jpg", ContentFile(image_temp.getvalue()), save=True)
          book.save()
          books = [book] 


    return books

  def __get_books_from_Google_Books_API(self,isbn):
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': 'isbn:' + isbn}
    response = requests.get(api_url, params=params)

    return response

  def __parse_partial_date(self,date_str):
    if date_str:
        for date_format in ("%Y-%m-%d", "%Y-%m"):
            try:
                return datetime.strptime(date_str, date_format).date()
            except ValueError:
                continue
    return None  

  def format_isbn(self,isbn):
    """
    isbnをXXXX-X-XXXX-XXXX-X.の形に変換する
    """
    isbn = str(isbn)

    parts = [isbn[:3], isbn[3:4], isbn[4:8], isbn[8:12], isbn[12:]]
    
    formatted_isbn = '-'.join(parts)

    return formatted_isbn
  # 
  def is_isbn13(self,str):
    return re.match(r'^(97(8|9))?\d{9}(\d|X)$', str.replace('-', ''))


  def convert_isbn10_to_isbn13(self,isbn10):
    # 厳密には違うがis_isbn13と長さが13であればisbn13として処理している
    if self.is_isbn13(isbn10) and len(isbn10) == 13:
      return isbn10

    isbn10.replace('-', '')
    """
     isbn10 を isbn13に変換する
    """
    isbn13_base = '978' + isbn10[:-1]

    checksum = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(isbn13_base)) % 10
    check_digit = str((10 - checksum) % 10)

    return isbn13_base + check_digit


  def test_print(self):
    print("hogehogehogehogehogehogehogehgeogh")