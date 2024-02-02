from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from django.contrib.auth.views import PasswordResetView

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import SignupForm
from api.models import Profile,Review,UserBook,Blog


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





class UserPageView(View):
    def get(self,request,pk):
        print(pk)
        user = User.objects.get(pk=pk)
        # userが読んだ本
        # userのツギヨム
        # userのnote    
        
        # 自分のページであればmypageに遷移する
        print("ユーザーページを表示します",user)
        profile = Profile.objects.get(user=user)
        reviews = Review.objects.filter(user=profile).select_related('user', 'book')
        
        next_books = UserBook.objects.filter(user=self.request.user).select_related("book")
        blogs = Blog.objects.filter(creator=profile).order_by("-created_at")

        context = {
            'profile': profile,
            'reviews': reviews,
            'next_books':next_books,
            "blogs":blogs,
        }

        return render(request, 'mypage.html', context)

class MyPageView(View):
        # 自分の読んだ本の一覧を表示する -> レビューをつけた本
        # 名前の変更
        # 自分が投稿したPollを表示する
        # ログアウト
        # アカウントの削除　
    
    def get(self,request):
        if not request.user.is_authenticated:
            #HttpResponseRedirect: redirectとの違いはアプリを超えてリダイレクトできることらしい
            return HttpResponseRedirect(reverse('login'))  

        profile = Profile.objects.get(user=request.user)

        # ユーザーのレビュー一覧を取得
        reviews = Review.objects.filter(user=profile).select_related('user', 'book')
        # 次に読むに登録している本を取得
        next_books = UserBook.objects.filter(user=self.request.user).select_related("book")
        blogs = Blog.objects.filter(creator=profile).order_by("-created_at")
 
        context = {
            'profile': profile,
           'reviews': reviews,
           'next_books':next_books,
           "blogs":blogs,
        }

        return render(request, 'mypage.html', context)

    def post(self,request):
        if not request.user.is_authenticated:
            #HttpResponseRedirect: redirectとの違いはアプリを超えてリダイレクトできることらしい
            return HttpResponseRedirect(reverse('login')) 

        username = self.request.POST.get("name")
        bio = self.request.POST.get("bio")
        image = request.FILES.get("image")

        profile = Profile.objects.get(user=request.user)
        profile.name = username
        profile.bio = bio
        if image:
            # 古い画像を削除する
            profile.delete_old_image()
            profile.image = image 

        profile.save()

        

        return redirect ("account")

class AccountClass():
    # @staticmethod
    def get_profile(self,user):
        profile = Profile.objects.get(user=user)
        return profile

