from django.urls import path
from . import views
from .views import search,about,index,details
urlpatterns = [
    path('', index.HomeView.as_view(), name='index'),
    path('about/', about.AboutView.as_view(), name='about'),
    path('search/', search.SearchView.as_view(), name='search_books'),
    path('book/<uuid:pk>/', details.DetailsView.as_view(), name='book_detail'),
]

