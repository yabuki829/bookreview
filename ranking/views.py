from django.shortcuts import render
from api.models import Book

from api.views.index import get_top_books_by_reviews
from utils.book_service import BookService

# Create your views here.

# ランキングを表示する
    # 本のカテゴリごとのランキング？
    # メリット　ランキングを作りやすい？
    # デメリット　カテゴリが設定されてないやつが多い　英語で設定されている
    # 評価がいい本のランキング？
    # メリット　簡単に実装できる
    # デメリット　変化があまりない

    
    
# def index(request):
#   # ページングを実装する
#   # 無限スクロール
#   books = get_top_books_by_reviews(30)
  
#   return render(request,"ranking.html",{
#     "books":books
#   })


from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import JsonResponse

def index(request):
    print("")
    # 30日間の本を取得する
    books = get_top_books_by_reviews(30)

    page = request.GET.get('page', 1)
    paginator = Paginator(books, 20)  # 10冊ごとにページ分割
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
      print("エラー")
      books = paginator.page(1)
    except EmptyPage:
      print("ページがからです")
      books = paginator.page(paginator.num_pages)

    if request.is_ajax():
      book_servise = BookService(request)
      books_data = [{
        'id': book.id,
        'title': book.title,
        # 'image_url': book.image.url if book.image else None,
        "isbn_10":book_servise.convert_isbn13_to_isbn10(book.isbn)
        } for book in books.object_list]

      return JsonResponse({'books': books_data, 'has_next': books.has_next()})


    

    return render(request, "ranking.html", {"books": books})
