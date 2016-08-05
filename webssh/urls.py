from django.conf.urls import url
# from . import views
from webssh.views import index,ws

urlpatterns = [

    url(r'index',index),
    url(r'ws',ws)
]
