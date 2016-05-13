from django.conf.urls import url
# from . import views
from triWeb.views import sayHi, current_time, cpu, disk, main_page, run_cmd, \
    ips, cos_config, cos_service, cos_analyze, testbeds

urlpatterns = [
    url(r'^$', sayHi, name='sayHi'),
    url(r'^time$', current_time),
    url(r'^cpu', cpu, name='cpu'),
    url(r'^disk', disk, name='disk'),
    url(r'main', main_page, name='remote_hosts'),
    url(r'run_cmd', run_cmd, name='run_cmd'),
    url(r'ips', ips, name='ips'),
    url(r'cos_config', cos_config, name='cos_config'),
    url(r'cos/service', cos_service, name='cos_service'),
    url(r'cos/analyze', cos_analyze, name='cos_analyze'),
    url(r'testbeds', testbeds, name='testbeds'),

]
