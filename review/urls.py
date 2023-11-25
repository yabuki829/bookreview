
from django.contrib import admin 
from django.urls import path,include
from . import views

urlpatterns = [
  path('',views.index , name='review'),
  path('book/<uuid:book_id>/', views.post_review, name='post_review'),
]
