
from django.views.generic import View


from ..models import Book,UserBook,Review
from django.shortcuts import render, get_object_or_404,redirect
from accounts.views import AccountClass

from utils.book_service import BookService

class DetailsView(View):
  def get(self,request,pk):
    # book　の isbnがpkの本を表示する
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    user_has_reviewed = False
    exists_in_next_read = False
    if request.user.is_authenticated:
      # ユーザーの「次に読む」リストに本が存在するかチェック
      exists_in_next_read = UserBook.objects.filter(user=self.request.user, book=book)
      # レビュー済みかどうかをチェック  
      account = AccountClass()
      user_has_reviewed = Review.objects.filter(book=book,user=account.get_profile(self.request.user))

      
    
    context = {
            'book': book,
            'reviews': reviews,
            'exists_in_next_read': exists_in_next_read,
            "user_has_reviewed":user_has_reviewed,
      }
    


    
    return render(request, "details_book.html", context)


  def post(self,request,pk):
    # ツギヨムに登録していなければ登録する
    # していれば解除する
    

    book_service = BookService(request)
    book = Book.objects.get(pk=pk)
    print(book,"をツギヨムに追加する")
    book_service.add_next_book_or_delete_book(book)


    return redirect('book_detail', pk=pk)  

