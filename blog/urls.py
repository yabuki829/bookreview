from django.urls import path

from .views import PostBlogView,DetailsBlogView


#url:  note/
urlpatterns = [
  path('create/',PostBlogView.as_view(), name='create_blog'),
  path('<str:pk>/',DetailsBlogView.as_view(), name='details_blog'),
]

