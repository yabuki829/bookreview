import re
import requests
from django.views.generic import View
from django.shortcuts import render

from django.utils.dateparse import parse_date

from django.shortcuts import render
from ..models import Book

class DetailsView(View):
  def get(self,request,pk):
    # book　の isbnがpkの本を表示する
    return render(request,"details.html")
  def post(self,request,pk):
    pass
