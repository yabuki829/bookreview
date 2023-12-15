from django.urls import path
from . import views
from .views import search,about,index,details,vote
urlpatterns = [
    path('', index.HomeView.as_view(), name='index'),
    path('about/', about.AboutView.as_view(), name='about'),
    path('search/', search.SearchView.as_view(), name='search_books'),
    path('book/<uuid:pk>/', details.DetailsView.as_view(), name='book_detail'),

    # TODO url変更する 
    path('poll_vote/<int:poll_id>/', vote.poll_vote, name='poll_vote'),
    path('create_poll/', vote.create_poll, name='create_poll'),
    path('poll_results/<int:poll_id>/', vote.poll_results, name='poll_results'),
]

