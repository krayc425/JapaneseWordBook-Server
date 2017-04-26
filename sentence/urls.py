from django.conf.urls import url

from . import views
from . import WordSentence

urlpatterns = [
    url(r'^(.*)$', WordSentence.wordSentence),
]