from django.urls import path

from .views import PostBlogView,DetailsBlogView,BlogListView


#url:  note/
# urlはblogではなくnoteを使っている
urlpatterns = [
  path('',         BlogListView.as_view(), name='blog_list'),
  path('create/',  PostBlogView.as_view(), name='create_blog'),
  path('<str:pk>/',DetailsBlogView.as_view(), name='details_blog'),
]

