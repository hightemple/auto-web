from django.conf.urls import url
# from . import views
from triWeb.views import sayHi, current_time, cpu, disk, remote_hosts, run_cmd, \
    ips, cmd_result, checkconfig_off_service

urlpatterns = [
    url(r'^$', sayHi, name='sayHi'),
    url(r'^time$', current_time),
    url(r'^cpu', cpu, name='cpu'),
    url(r'^disk', disk, name='disk'),
    url(r'remote', remote_hosts, name='remote_hosts'),
    url(r'run_cmd', run_cmd, name='run_cmd'),
    url(r'cmd_result', cmd_result, name='cmd_result'),
    url(r'ips', ips, name='ips'),
    url(r'checkconfig_off_service',checkconfig_off_service),

]
