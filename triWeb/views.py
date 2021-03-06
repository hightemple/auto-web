from functools import reduce
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import threading
import json
import yaml
import queue

from os.path import dirname, abspath, join
from .tools.testbed import TestBed

# Create your views here.
from triWeb.tools.pxssh import ssh2
from triWeb.models import TestBedModel, DeviceModel, CliModel


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




def main_page(reqeust):
    tbs = TestBedModel.objects.all()

    tb2devices = dict()


    for tb in tbs:
        devices = DeviceModel.objects.filter(testbed=tb)
        type2devices = {}
        type_list = get_devices_types(devices)
        for dv_type in type_list:
            type2devices[dv_type] = DeviceModel.objects.filter(type=dv_type, testbed=tb)
        tb2devices[tb] = type2devices

    return render(reqeust, 'triWeb/main_page.html', {'tb2devices': tb2devices})

def test(reqeust):
    tbs = TestBedModel.objects.all()

    tb2devices = dict()


    for tb in tbs:
        devices = DeviceModel.objects.filter(testbed=tb)
        type2devices = {}
        type_list = get_devices_types(devices)
        for dv_type in type_list:
            type2devices[dv_type] = DeviceModel.objects.filter(type=dv_type, testbed=tb)
        tb2devices[tb] = type2devices

    return render(reqeust, 'triWeb/test.html', {'tb2devices': tb2devices})

def get_devices_types(devices):
    type_list = []
    for dv in devices:
        if dv.type not in type_list:
            type_list.append(dv.type)
    return type_list


def cos_analyze(request):
    now = datetime.datetime.now()
    html = "<html><body> It is now : %s </body></html>" % now
    return HttpResponse(html)



def run_cmd(request):
    cmd = request.POST['cmd'].strip()
    dv_ssh_info_list=[]

    device_info_list = []
    device_string_list = []
    #get selected devices
    for key in request.POST.keys():
        if "____" in key:
            device_string_list.append(key)

    for dv_str in device_string_list:
        dv_info = dv_str.split("____")

        try:
            dv = DeviceModel.objects.get(testbed_id=dv_info[0],name=dv_info[1])

        except DeviceModel.DoesNotExist:
            pass
        else:
            dv_info.append(dv.ip)
            dv_ssh_info_list.append({'ip':dv.ip,'user':dv.user,'password':dv.password})
            device_info_list.append(dv_info)



    rst_dict = pssh_cmd(request, dv_ssh_info_list, cmd)
    # rst_dict={}
    return render(request, 'triWeb/run_cmd.html', {'device_info_list':device_info_list,
                                                   'cmd': cmd, 'rst_dict': rst_dict})




def pssh_cmd(request, dv_info_list, cmd):
    thread_list = list()
    # q = queue.Queue()
    rst_dict = dict()

    def sig_ssh(ip, username, password, cmd):
        rtn = ssh2(ip, username, password, cmd)
        rst_dict[ip] = rtn

    for dv in dv_info_list:
        thread_list.append(
            threading.Thread(target=sig_ssh, name="t_ssh_to_%s" % dv['ip'], args=(dv['ip'], dv['user'], dv['password'], cmd.strip())))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    return rst_dict


def get_sel_devices(request):
    tb_name = request.GET['Name']
    rtn = ''
    for device in DeviceModel.objects.filter(testbed__name=tb_name, type='cos'):
        rtn = rtn + '<li><strong>' + device.name + "  " + device.ip + '</strong></li>'
    return HttpResponse(rtn)


def testbeds(request,tb_name):
    APP_DIR = dirname(abspath(__file__))
    tb_dict = dict()
    for tbo in TestBedModel.objects.all():
        tb_dict[tbo.name]=tbo.path
    if tb_name in tb_dict.keys():
        fp=join(APP_DIR,"testbeds",tb_dict[tb_name])
        tb = TestBed()
        conf_dict = tb.load(fp)

        rtn_lst = tb.parse_to_json_tree(conf_dict)

    return render(request, 'triWeb/testbeds.html', {'jconf': json.dumps(rtn_lst)})

def retrieve_cli_type(request):
    obj_list = CliModel.objects.values('type').distinct()
    resp_json = []
    for obj in obj_list:
        resp_json.append({'label': obj['type'], 'value': obj['type']})

    return HttpResponse(json.dumps(resp_json))


def retrieve_cli_category(request):
    type = request.GET['tId']
    obj_list = CliModel.objects.filter(type=type).values('category').distinct()
    resp_json = []
    for obj in obj_list:
        resp_json.append({'label': obj['category'], 'value': obj['category']})

    return HttpResponse(json.dumps(resp_json))


def retrieve_cli_name(request):
    type = request.GET['tId']
    category = request.GET['cId']
    obj_list = CliModel.objects.filter(type=type,category=category).values('name','content').distinct()
    resp_json = []
    for obj in obj_list:
        resp_json.append({'label': obj['name'], 'value': obj['content']})


    return HttpResponse(json.dumps(resp_json))
