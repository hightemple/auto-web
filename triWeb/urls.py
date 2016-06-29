from django.conf.urls import url
# from . import views
from triWeb.views import sayHi, current_time, cpu, disk, main_page, run_cmd, \
    get_sel_devices, cos_analyze, testbeds, test, \
    retrieve_cli_type, retrieve_cli_category , retrieve_cli_name

urlpatterns = [
    url(r'^$', sayHi, name='sayHi'),
    url(r'^time$', current_time),
    url(r'^cpu', cpu, name='cpu'),
    url(r'^disk', disk, name='disk'),
    url(r'main', main_page, name='remote_hosts'),
    url(r'run_cmd', run_cmd, name='run_cmd'),
    url(r'get_sel_devices', get_sel_devices, name='ips'),
    url(r'cos/analyze', cos_analyze, name='cos_analyze'),
    url(r'testbeds/(\S+)', testbeds, name='testbeds'),


    url(r'test',test),
    url(r'get/cli/type', retrieve_cli_type),
    url(r'get/cli/category', retrieve_cli_category),
    url(r'get/cli/name', retrieve_cli_name)
]
