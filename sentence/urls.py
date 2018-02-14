from django.conf.urls import url

from . import WordSentenceNew

urlpatterns = [
    url(r'^(.*)$', WordSentenceNew.wordSentence),
]