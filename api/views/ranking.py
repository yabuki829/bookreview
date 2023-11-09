from django.shortcuts import render
from django.views.generic import View

class RankingView(View):
  def get(self,request):
    # なんのランキングを表示する？
    # 評価がいい本のランキング？
    
    return render(request, 'ranking.html')