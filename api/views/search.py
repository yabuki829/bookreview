import re
import requests
from django.views.generic import View
from django.shortcuts import render

from django.shortcuts import render


from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.book_service import BookService



class SearchView(View):
  def get(self,request):
   
    # 検索クエリを取得
    query = request.GET.get('q', '') 
    # TODO 空白を入れて検索している場合も今後考えたい and検索

    print("検索:",query)
    book_service = BookService(request)
    if query:
      if book_service.is_isbn13(query):
        query = query.replace('-', '')
        books = book_service.get_book_with_isbn(query)
        print("取得完了",books)
      else:
        books = book_service.get_books_with_title(query)
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
