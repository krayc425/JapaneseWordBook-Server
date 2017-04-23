from django.conf.urls import url

from . import views
from . import WordSearch

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(.*)$', WordSearch.searchWord),
]