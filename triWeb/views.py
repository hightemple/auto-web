from functools import reduce
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import threading
import queue

# Create your views here.
from triWeb.tools.pxssh import ssh2


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
    return render(reqeust, 'triWeb/main_page.html', {'groups': groups, 'cmds': cmd_dict})


def run_cmd(request):
    cmd = request.POST['cmd']

    ip_lst = []
    grp_lst = []

    for grp in groups.keys():
        if request.POST.get(grp):
            grp_lst.append(grp)
            for ip in groups[grp]:
                ip_lst.append(ip)
    rst_dict = pssh_cmd(request, ip_lst, cmd)
    return render(request, 'triWeb/run_cmd.html', {'ip_list': ip_lst, 'grp_list': grp_lst,
                                                   'cmd': cmd, 'rst_dict': rst_dict})


def cos_config(request):
    cmd = cmd_dict[request.POST.get('sel_cmd')]
    grp = request.POST.get('sel_grp')
    ip_lst = groups[grp]
    grp_lst = list(grp)

    rst_dict = pssh_cmd(request,ip_lst,cmd)

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
    group = request.GET['Name']
    rtn = ''
    for ip in groups[group]:
        rtn = rtn + '<li>' + ip + '</li>'
    return HttpResponse(rtn)
