from django.urls import path

from .views import PostBlogView,DetailsBlogView,BlogListView,ShowTagsView,Show_Blog_Tag


#url:  note/
# urlはblogではなくnoteを使っている
urlpatterns = [
  path('',                  BlogListView.as_view(), name='blog_list'),
  path('create/',           PostBlogView.as_view(), name='create_blog'),
  path('tags/<str:tag>',    Show_Blog_Tag.as_view(), name='show_blog_tag'),
  path('tags/',             ShowTagsView.as_view(), name='show_all_tags'),
  path('<str:pk>/',         DetailsBlogView.as_view(), name='details_blog'),

]

