
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

    user_has_reviewed = False
    if request.user.is_authenticated:
      user_has_reviewed = book.reviews.filter(user=request.user.profile).exists()

    context = {
            'book': book,
            'reviews': reviews,
            'user_has_reviewed': user_has_reviewed,
    }
    return render(request, "details.html", context)

