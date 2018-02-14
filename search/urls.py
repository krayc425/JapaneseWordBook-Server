from django.conf.urls import url

from . import WordSearchNew

urlpatterns = [
    url(r'^(.*)$', WordSearchNew.searchWord),
]