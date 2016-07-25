from django.conf.urls import url
# from . import views
from webssh.views import index

urlpatterns = [

    url(r'index',index),
]
