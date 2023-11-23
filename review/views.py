from django.shortcuts import render
from api.models import Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
  reviews = Review.objects.all()

  paginator = Paginator(reviews, 20)
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
