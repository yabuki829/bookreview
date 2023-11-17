from django.urls import path
from .views import poll_vote,create_poll,poll_results,poll_list
urlpatterns = [
  path('', poll_list, name='poll'),
  path('vote/<int:poll_id>/', poll_vote, name='poll_vote'),
  path('create/', create_poll, name='create_poll'),
  path('results/<int:poll_id>/',poll_results, name='poll_results'),
]

