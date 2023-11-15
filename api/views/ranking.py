from django.shortcuts import render
from django.views.generic import View

class RankingView(View):
  def get(self,request):
    # 本のカテゴリごとのランキング？
    # メリット　ランキングを作りやすい？
    # デメリット　カテゴリが設定されてないやつが多い　英語で設定されている
    # 評価がいい本のランキング？
    
    
    return render(request, 'ranking.html')