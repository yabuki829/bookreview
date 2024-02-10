

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
6. add_next_book(book)
    次に読む本に追加する
7. write_review(book,content,rateing):
    もしツギヨムに本が追加されて入れば削除する
    レビューを書く

"""

import re
import requests
from datetime import datetime
from django.utils.crypto import get_random_string
# 画像系
from django.core.files.base import ContentFile
from io import BytesIO

from api.models import Book,Category,UserBook,Review




class BookService():
  def __init__(self, request=None):
        self.request = request
        
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
   
 

        published_date = book_info.get('publishedDate', '')
        # 日付を修正
        print(published_date)
        published_at = self.__parse_partial_date(published_date)
        print(published_at)
        category_name_en = book_info.get('categories', [''])[0]
        # カテゴリを作成
        category, created = Category.objects.get_or_create(name_en=category_name_en)
        title = book_info.get('title', '')
        print("タイトル：",title)
        book = Book(
          id = self.create_id(22),
          isbn=isbn13,
            title=title,
            subTitle=book_info.get("subtitle",""),
            author=book_info.get('authors', [''])[0],  # 代表者一名のみ取得
            description=book_info.get('description', ''),
            published_at=published_at,
            category=category
        )
        
        book.save()
      
        books = [book] 


    return books


  def __get_books_from_Google_Books_API(self,isbn):
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': 'isbn:' + isbn}
    response = requests.get(api_url, params=params)

    return response



  def __parse_partial_date(self, date_str):
    if date_str:
        # 年-月-日、年-月、年 の順でパースを試みる
        for date_format in ("%Y-%m-%d", "%Y-%m", "%Y"):
            try:
                parsed_date = datetime.strptime(date_str, date_format).date()
                # 年のみの場合、1月1日を追加
                if date_format == "%Y":
                    return datetime(parsed_date.year, 1, 1).date()
                return parsed_date
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
  
  def add_next_book_or_delete_book(self,book):
    # ツギヨムに追加する
    user = self.request.user

    next_book_to_read, created = UserBook.objects.get_or_create(user=user, book=book)
    if not created:
      # ツギヨムに登録済みなので削除する
      print("ツギヨムから削除しました")
      next_book_to_read.delete()
    

  def write_review(self,content,book,rating):
    # もしツギヨムに追加されていればツギヨムから削除する
    exists_in_next_read = UserBook.objects.filter(user=self.request.user, book=book)
    if exists_in_next_read:
      exists_in_next_read.delete()

    Review.objects.create(
                id = self.create_id(22),
                user=self.request.user.profile,  # ログインしているユーザーのプロフィール
                content=content,
                rating=rating,
                book=book
            )
    

  def convert_isbn13_to_isbn10(self,isbn13):
    if not isbn13.startswith('978') or len(isbn13) != 13:
        raise ValueError("ISBN-13 must start with '978' and be 13 characters long.")
    isbn10_base = isbn13[3:-1]  # 最初の3文字を取り除き、チェックディジットを除外
    checksum = 0
    for i, char in enumerate(isbn10_base, start=1):  # ISBN-10のチェックサム計算
        checksum += i * int(char)
    checksum %= 11
    if checksum == 10:
        checksum = 'X'
    else:
        checksum = str(checksum)
    return isbn10_base + checksum

  def create_id(self,n):
    return get_random_string(n)