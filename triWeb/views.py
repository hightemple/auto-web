import paramiko

import os
from django.shortcuts import render
from django.http import HttpResponse
import datetime


# Create your views here.

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
        'xuan': [88,'hubei'],
        'fei' : [70, 'hunan']
    }

    return render(request, 'triWeb/disk.html', {'disk_usage': disk_usage, 'name_dict':name_dict})

groups = dict()
groups['crdc'] = ['10.74.124.92','10.74.124.94','10.74.124.96','10.74.124.98','10.74.124.100','10.74.124.102']


def remote_hosts(reqeust):
    return render(reqeust, 'triWeb/remote_hosts.html', {'groups': groups})


def run_cmd(request):
    ip_lst = []
    grp_lst = []
    cmd = request.POST['cmd']
    result = ''
    for grp in groups.keys():
        if request.POST.get(grp):
            grp_lst.append(grp)
            for ip in groups[grp]:
                ip_lst.append(ip)


    for ip in ip_lst:
        ssh_rst = ssh2(ip,'root','rootroot',cmd)
        result = result + "\n" + ip + ": \n" + ssh_rst.decode('ascii')


    return render(request, 'triWeb/run_cmd.html', {'ip_list':ip_lst, 'grp_list':grp_lst,
                                                   'cmd': cmd, 'result':result})


def cmd_result(request):

    return HttpResponse('<li>good<li>')

def ips(request):
    group = request.GET['Name']
    rtn = ''
    for ip in groups[group]:
        rtn = rtn + '<li>' + ip + '</li>'
    return HttpResponse(rtn)


def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #           stdin.write("Y")   #简单交互，输入 ‘Y’
        return stdout.read()
        #        for x in  stdout.readlines():
        #          print x.strip("n")
        return '%stOKn'%(ip)
        ssh.close()
    except:
        return '%stErrorn'%(ip)
