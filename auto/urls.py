from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'auto.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'', include('blog.urls')),
                       url(r'^webssh/', include('webssh.urls')),
                       url(r'', include('triWeb.urls'))

                       )
