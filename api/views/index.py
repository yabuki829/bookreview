from django.shortcuts import render
from django.views.generic import View

from ..models import Profile,Blog

from blog.views import BlogClass
class HomeView(View):
  def get(self,request):
    # 最近のレビューを表示する
    # 最近のpollを表示する
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7) 
    top_books_7 = get_top_books_by_reviews(start_date, end_date)

    start_date = end_date - timedelta(days=30) 
    top_books_30 = get_top_books_by_reviews(start_date, end_date)

    profile = Profile.objects.get(id="4")

    blog_class = BlogClass()
    tag = blog_class.get_tag("お知らせ")
    blogs = reversed(Blog.objects.filter(creator=profile,).order_by("created_at")[:5])


    return render(request, 'home.html', {
        "top_books_7": top_books_7,
        "top_books_30":top_books_30,
        "blogs":blogs,
        
        }
    )


from django.db.models import Count
from ..models import Book, Review
from django.utils import timezone
from datetime import timedelta




def get_top_books_by_reviews(start_date, end_date):
    # 期間中のレビューをつけられた本のランキングを返す
    # annotateでレビューの数を数えてソートする
    return Book.objects.filter(
        reviews__created_at__range=(start_date, end_date)
    ).annotate(
        num_reviews=Count("reviews")
    ).order_by("-num_reviews")




