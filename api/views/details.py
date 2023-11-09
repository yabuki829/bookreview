
from django.views.generic import View
from django.shortcuts import render


from django.shortcuts import render
from ..models import Book
from django.shortcuts import render, get_object_or_404

class DetailsView(View):
  def get(self,request,pk):
    # book　の isbnがpkの本を表示する
    book = get_object_or_404(Book, pk=pk)
    print(book.title)
    reviews = book.reviews.all() 

    context = {
      'book': book,
      'reviews': reviews,  
    }

        # レンダリングされたレスポンスを返す
    return render(request, "details.html", context)

  def post(self,request,pk):
    pass
