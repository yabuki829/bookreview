from django.shortcuts import render
from rest_framework import views, status
# Create your views here.
from django.views.generic import View

from rest_framework import views
from .models import Profile, Book, Review
from .serializers import ProfileSerializer, BookSerializer, ReviewSerializer
from rest_framework.response import Response

class ProfileAPIView(views.APIView):
  def get(self, request, format=None):
    return Response("戻り値")

  def post(self, request, format=None):  
      return Response("戻り値")


class BookAPIView(views.APIView):
  def get(self, request, format=None):
    # 本の一覧を表示する
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):  
      return Response("戻り値")

class ReviewAPIView(views.APIView):
  def get(self, request, format=None):
    return Response("戻り値")

  def post(self, request, format=None):  
      return Response("戻り値")


class HomeView(View):
  def get(self,request):
    return render(request, 'home.html')

class AboutView(View):
  def get(self,request):
    return render(request, 'about.html')

class LoginView(View):
  def get(self,request):
    return render(request, 'login.html')

class RegisterView(View):
  def get(self,request):
    return render(request, 'register.html')  
