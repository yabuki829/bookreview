
from django.contrib import admin 
from django.contrib.auth import views
from django.urls import path,include
from .views import CustomPasswordResetView,SignUpView,activate,MyPageView

urlpatterns = [
    path("",MyPageView.as_view(),name="account"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.LogoutView.as_view(),name="logout"),

    path("signup/",SignUpView.as_view(),name="signup"),
    path("activate/<uuid:token>/", activate, name="activate"),  # 追加
    path("password_change/",views.PasswordChangeView.as_view(),name="password_change",),
    path("password_change/done/",views.PasswordChangeDoneView.as_view(),name="password_change_done"),

    # パスワード再設定
    path("password_reset/",CustomPasswordResetView.as_view(),name="password_reset"),
    path("password_reset/done/",views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("reset/done/",views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

   
]
