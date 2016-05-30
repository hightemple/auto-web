from functools import reduce
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import threading
import json
import yaml
import queue
from .tools.testbed import TestBed

# Create your views here.
from triWeb.tools.pxssh import ssh2
from triWeb.models import TestBedModel, DeviceModel


def sayHi(request):
    return HttpResponse("Hello World!")


def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body> It is now : %s </body></html>" % now
    return HttpResponse(html)


def cpu(request):
    cpu_status = os.popen('sar 1').read()
    # html_cpu = "<html> %s </html>"%cpu_status

    return render(request, 'triWeb/cpu_status.html', {'cpu_status': cpu_status})


def disk(request):
    disk_usage = os.popen('df -h').read()
    name_dict = {
        'xuan': [88, 'hubei'],
        'fei': [70, 'hunan']
    }

    return render(request, 'triWeb/disk.html', {'disk_usage': disk_usage, 'name_dict': name_dict})


groups = dict()
# groups['crdc'] = ['10.74.124.92','10.74.124.94','10.74.124.96','10.74.124.98','10.74.124.100','10.74.124.102']
groups['crdc'] = ['10.74.124.92', '10.74.124.94', '10.74.124.96']
cmd_dict = {
    'Show all service': "service --status-all",
    'Show intalled packages': 'cos_pkgs',
}


def main_page(reqeust):
    tbs = TestBedModel.objects.all()

    tb2devices = dict()
    for tb in tbs:
        tb2devices[tb] = DeviceModel.objects.filter(type='cos', testbed=tb)

    return render(reqeust, 'triWeb/main_page.html', {'tb2devices': tb2devices, 'cmds': cmd_dict})


def cos_service(request):
    return render(request, 'triWeb/cos_service.html', {'groups': groups, 'cmds': cmd_dict})


def cos_analyze(request):
    now = datetime.datetime.now()
    html = "<html><body> It is now : %s </body></html>" % now
    return HttpResponse(html)


def retrieve_cmd(request):
    sel_cmd = request.GET['Cmd']
    exec_cmd = cmd_dict[sel_cmd]
    return HttpResponse(exec_cmd)


def run_cmd(request):
    cmd = request.POST['cmd']

    ip_lst = []
    tb_lst = []

    for tb in TestBedModel.objects.all():
        if tb.name in request.POST.keys():
            tb_lst.append(tb.name)
            for dv in DeviceModel.objects.filter(type='cos', testbed=tb):
                ip_lst.append(dv.ip)

    rst_dict = pssh_cmd(request, ip_lst, cmd)
    return render(request, 'triWeb/run_cmd.html', {'ip_list': ip_lst, 'tb_list': tb_lst,
                                                   'cmd': cmd, 'rst_dict': rst_dict})


def cos_config(request):
    cmd = cmd_dict[request.POST.get('sel_cmd')]
    grp = request.POST.get('sel_grp')
    ip_lst = groups[grp]
    grp_lst = list(grp)

    rst_dict = pssh_cmd(request, ip_lst, cmd)

    return render(request, 'triWeb/run_cmd.html', {'ip_list': ip_lst, 'grp_list': grp_lst,
                                                   'cmd': cmd, 'rst_dict': rst_dict})


def pssh_cmd(request, ips, cmd):
    thread_list = list()
    # q = queue.Queue()
    rst_dict = dict()

    def sig_ssh(ip, username, password, cmd):
        rtn = ssh2(ip, username, password, cmd)
        rst_dict[ip] = rtn

    for ip in ips:
        thread_list.append(
            threading.Thread(target=sig_ssh, name="t_ssh_to_%s" % ip, args=(ip, 'root', 'rootroot', cmd)))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    return rst_dict


def ips(request):
    tb_name = request.GET['Name']
    rtn = ''
    for device in DeviceModel.objects.filter(testbed__name=tb_name, type='cos'):
        rtn = rtn + '<li><strong>' + device.name + "  " + device.ip + '</strong></li>'
    return HttpResponse(rtn)


def testbeds(request,tb_name):

    tb_dict = dict()
    for tbo in TestBedModel.objects.all():
        tb_dict[tbo.name]=tbo.path
    if tb_name in tb_dict.keys():
        fp=tb_dict[tb_name]
        tb = TestBed()
        conf_dict = tb.load(fp)

        rtn_lst = tb.parse_to_json_tree(conf_dict)

    return render(request, 'triWeb/testbeds.html', {'jconf': json.dumps(rtn_lst)})
