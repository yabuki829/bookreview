
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
    reviews = book.reviews.all().order_by('-created_at')

    context = {
      'book': book,
      'reviews': reviews,  
    }
    return render(request, "details.html", context)

  def post(self,request,pk):
    pass
