from django.shortcuts import render

# Create your views here.

from django.contrib.auth.views import PasswordResetView

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import SignupForm
from api.models import Profile,Review


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'



from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic import View
User = get_user_model()

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        # メールを送信する
        #TODO 本番環境ではurlを変える
        print("メールを送信しました。")
        send_mail(
            'アカウントの確認',
            f'認証URL: http://127.0.0.1:8000/accounts/activate/{user.activation_token}/',
            'from-email@example.com',
            [user.email],
            fail_silently=False,
        )
        return render(self.request, 'registration/signup_done.html')

def activate(request, token):
    print("activateします")
    try:
        user = User.objects.get(activation_token=token)
        user.is_active = True
        user.save()
        # profileを作成する
        profile = Profile.objects.create(user=user,name="No Name")
        profile.save()
        return HttpResponse("アカウントが認証されました！")
    except User.DoesNotExist:
        return HttpResponse("無効なトークンです。")







class MyPageView(View):
        # 自分の読んだ本の一覧を表示する -> レビューをつけた本
        # 名前の変更
        # 自分が投稿したPollを表示する
        # ログアウト
        # アカウントの削除　
        
    def get(self,request):
        profile = Profile.objects.get(user=request.user)

        # ユーザーのレビュー一覧を取得

        book_count_per_bookshelf = 4
        reviews = Review.objects.filter(user=profile).select_related('book')
        review_chunks = [reviews[i:i + book_count_per_bookshelf] for i in range(0, len(reviews), book_count_per_bookshelf)]
        print(review_chunks)
        context = {
            'profile': profile,
           'review_chunks': review_chunks
        }

        return render(request, 'mypage.html', context)

