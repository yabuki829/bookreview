import re
import requests
from django.views.generic import View
from django.shortcuts import render

from django.core.files.base import ContentFile
from io import BytesIO
from django.utils.dateparse import parse_date

from django.shortcuts import render
from ..models import Book,Category

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from datetime import datetime

def parse_partial_date(date_str):
    if date_str:
        for date_format in ("%Y-%m-%d", "%Y-%m"):
            try:
                return datetime.strptime(date_str, date_format).date()
            except ValueError:
                continue
    return None  



def get_books_from_Google_Books_API(isbn):
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': 'isbn:' + isbn}
    response = requests.get(api_url, params=params)

    return response


class SearchView(View):
  def get(self,request):
    print("isbn",format_isbn("9784286245720"))
    # 検索クエリを取得
    query = request.GET.get('q', '') 
    # TODO 空白を入れて検索している場合もm今後考えたい

    print("検索:",query)
    if query:
      if re.match(r'^(97(8|9))?\d{9}(\d|X)$', query.replace('-', '')):
        print("isbnでの検索です")
        query = query.replace('-', '')
        books = Book.objects.filter(isbn=query)
        # 本が登録されてない場合GoogleBooksAPIから本情報を取得する
        if not books.exists() and query:
         
          response = get_books_from_Google_Books_API(query)

          if response.status_code == 200:
              print("取得が完了しました")
              result = response.json()
              items = result.get('items', [])

              if items:
                  book_info = items[0]['volumeInfo']

                  # 画像処理

                  # 画像がない場合エラーになる

                  print(book_info)
                  image_url = book_info.get('imageLinks', {}).get('thumbnail')
                  print("画像だよ",image_url)
                  if image_url:
                      image_response = requests.get(image_url)
                      if image_response.status_code == 200:
                          # BytesIOを使用して一時ファイルを作成する
                          image_temp = BytesIO(image_response.content)
                  else:
                    pass

                  # 出版日処理
                  
                  published_date = book_info.get('publishedDate', '')
                  published_at = parse_partial_date(published_date)
         
                  category_name_en = book_info.get('categories', [''])[0]
                  category, created = Category.objects.get_or_create(name_en=category_name_en)
                
                  title = book_info.get('title', '')
                  print("タイトル:",title)

                  # もし同じタイトルがあれば追加しない
                  books = Book.objects.filter(title=title)
                  if len(books) != 0 :
                    print("既に同じタイトルがあります")
                    books
                  else:
                    book = Book(
                        isbn=query,
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
              else:
                print("本の情報がありませんでした。")
   
      else:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = []
    
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page', 1)
    #　選択ページの両側には3コ表示する
    onEachSide = 3
    #　左右両端には2コ表示する
    onEnds = 2 

    try:
            books_page = paginator.page(page_number)
    except PageNotAnInteger:
            books_page = paginator.page(1)
    except EmptyPage:
            books_page = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)

    context = {
            'books': books_page,  
            'query': query,
            'page_range': page_range,  
    }

    return render(request, 'search.html', context)




def format_isbn(isbn):
    """
    isbnをXXXX-X-XXXX-XXXX-X.の形に変換する
    """
    isbn = str(isbn)

    parts = [isbn[:3], isbn[3:4], isbn[4:8], isbn[8:12], isbn[12:]]
    
    formatted_isbn = '-'.join(parts)

    return formatted_isbn


