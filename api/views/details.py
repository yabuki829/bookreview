
from django.views.generic import View


from ..models import Book,UserBook
from django.shortcuts import render, get_object_or_404,redirect

class DetailsView(View):
  def get(self,request,pk):
    # book　の isbnがpkの本を表示する
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')

    user_has_reviewed = False
    if request.user.is_authenticated:
      # ユーザーの「次に読む」リストに本が存在するかチェック
      exists_in_next_read = UserBook.objects.filter(user=self.request.user, book=book)
      user_has_reviewed = book.reviews.filter(user=request.user.profile).exists()



    context = {
            'book': book,
            'reviews': reviews,
            'exists_in_next_read': exists_in_next_read,
    }
    return render(request, "details_book.html", context)


  def post(self,request,pk):
    # ツギヨムに登録していなければ登録する
    # していれば解除する
    
    print(pk,"を次に読む本に追加する")

    book = Book.objects.get(pk=pk)
    user = self.request.user

    next_book_to_read, created = UserBook.objects.get_or_create(user=user, book=book)

    # 
    if not created:
      # ツギヨムに登録済みなので削除する
      print("ツギヨムから削除しました")
      next_book_to_read.delete()
    else:
      print("ツギヨムに追加する")
    
  


    return redirect('book_detail', pk=pk)  

