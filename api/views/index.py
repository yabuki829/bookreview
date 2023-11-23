from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
  def get(self,request):
    # 最近のレビューを表示する
    # 最近のpollを表示する
    
    return render(request, 'home.html')