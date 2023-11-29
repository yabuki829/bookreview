from django.shortcuts import render
from api.models import Review,Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# レビュー画面のトップページ
def index(request):

  reviews = Review.objects.all().order_by('-created_at')


  paginator = Paginator(reviews, 12)
  page_number = request.GET.get('page', 1)
    #　選択ページの両側には3コ表示する
  onEachSide = 3
    #　左右両端には2コ表示する
  onEnds = 2 
  try:
      review_page = paginator.page(page_number)
  except PageNotAnInteger:
      review_page = paginator.page(1)
  except EmptyPage:
      review_page = paginator.page(paginator.num_pages)

  page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)

  context = {
      'reviews': review_page,  
      'page_range': page_range,  
    }

    
  return render(request, 'index.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def post_review(request, book_id):
    print("レビューを投稿するぜ")
    book = get_object_or_404(Book, pk=book_id)
    print(book)
    if request.method == 'POST':
        print("POST")
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        print(content,rating)
        if content and rating:
            Review.objects.create(
                user=request.user.profile,  # ログインしているユーザーのプロフィール
                content=content,
                rating=rating,
                book=book
            )
            print("投稿が完了しました")
            return redirect('book_detail', pk=book.id)

    return render(request, 'review_form.html', {'book': book})