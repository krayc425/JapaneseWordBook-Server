from django.conf.urls import url

from . import views
from . import WordSound

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(.*)$', WordSound.soundWord),
]