from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
  def get(self,request):
    # 最近のレビューを表示する
    # 最近のpollを表示する
    end_date = timezone.now()
    # 30にち間の場合
    start_date = end_date - timedelta(days=7) 
    top_books = get_top_books_by_reviews(start_date, end_date)


    print(top_books)
    return render(request, 'home.html', {'top_books': top_books})


from django.db.models import Count
from ..models import Book, Review
from django.utils import timezone
from datetime import timedelta

def get_top_books_by_reviews(start_date, end_date):
    # 期間中のレビューをつけられた本のランキングを返す
    return Book.objects.filter(
        reviews__created_at__range=(start_date, end_date)
    ).annotate(
        num_reviews=Count('reviews')
    ).order_by('-num_reviews')




