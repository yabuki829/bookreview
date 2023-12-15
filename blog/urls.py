from django.urls import path

from .views import PostBlogView,DetailsBlogView,CommentBlogView



urlpatterns = [
  path('create',PostBlogView.as_view(), name='create_blog'),
  path('<uuid:pk>/',PostBlogView.as_view(), name='details_blog'),
]

