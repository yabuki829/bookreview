from django.shortcuts import render
from django.views.generic import View

from ..models import Profile,Blog,Tag

from blog.views import BlogClass
class HomeView(View):
  def get(self,request):
    # 最近のレビューを表示する
    # 最近のpollを表示する
   
    top_books_7 = get_top_books_by_reviews(7)

    top_books_30 = get_top_books_by_reviews(100)

    news_blogs = get_news_blog()
    blogs = get_blogs(12)


    return render(request, 'home.html', {
        "latest_books": get_latest_books(30),
        "top_books_7": top_books_7,
        "top_books_30":top_books_30,
        "news_blogs":news_blogs,
        "blogs":blogs,
        }
    )


from django.db.models import Count
from ..models import Book, Review
from django.utils import timezone
from datetime import timedelta




def get_top_books_by_reviews(days:int):
    end_date = timezone.now() 
    start_date = end_date - timedelta(days=days) 
    # 期間中のレビューをつけられた本のランキングを返す
    # annotateでレビューの数を数えてソートする
    book = Book.objects.filter(
        reviews__created_at__range=(start_date, end_date)
    ).annotate(
        num_reviews=Count("reviews")
    ).order_by("-num_reviews")

    print(book)
    return book


# 公式のお知らせブログを取得する
def get_news_blog():
    # お知らせを取得する
    blog_class = BlogClass()
    tag = blog_class.get_tag("お知らせ")

    profile = Profile.objects.get(id="4")
    news_blogs = reversed(Blog.objects.filter(creator=profile,tag=tag).order_by("created_at")[:10])

    return news_blogs



def get_blogs(count:int):
    tag = Tag.objects.get(title="お知らせ")
    blogs = Blog.objects.exclude(tag=tag).order_by('-created_at')[:count]

    return blogs



# データベースから最新の本を取得する 
def get_latest_books(day):
    # 発売日が30日後のやつまで表示する
    end_date = timezone.now() + timedelta(days=day) 
    start_date = end_date - timedelta(days=120) 
    books = Book.objects.filter(published_at__range=(start_date,end_date))
    return books


    