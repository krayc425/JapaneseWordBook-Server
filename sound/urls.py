from django.conf.urls import url

from . import views
from . import WordSound

urlpatterns = [
    url(r'^(.*)$', WordSound.soundWord),
]