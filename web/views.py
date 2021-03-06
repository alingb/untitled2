# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import re
from subprocess import Popen, PIPE

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse
from detail.models import *


@login_required
def index(req):
    return render(req, "html/index.html")


def logout_user(req):
    logout(req)
    return redirect(reverse('login'))


def check_password(passwd):
    if re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$', passwd):
        return True
    else:
        return False


def signup(request):
    if request.method == "GET":
        return render(request, 'web/signup.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        rpassword = request.POST.get('checkpassword', None)
        try:
            User.objects.get(username=username)
            return render(request, 'web/signup.html', {"error": u'用户已注册!'})
        except:
            pass
        if rpassword != password:
            return render(request, 'web/signup.html', {"error": u"两次密码输入不一样"})
        if not check_password(password):
            return render(request, 'web/signup.html', {"error": u"password  is invalid"})
        passwd = make_password(password)
        User.objects.create(username=username,
                            password=passwd,
                            is_active=True,
                            is_staff=True)
        return redirect(reverse('login'))


def login_user(request):
    if request.method == 'GET':
        return render(request, 'web/login.html')
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember = request.POST.get('remember', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            return redirect(reverse('index'))
        else:
            return render(request, 'web/login.html', {'error': u'用户名或密码错误!'})


@login_required
def base(req):
    return render(req, 'web/index.html')


@login_required
def cpuStat(req):
    return render(req, 'web/cpustat.html')


@login_required
def memStat(req):
    return render(req, 'web/memstat.html')


@login_required
def diskStat(req):
    return render(req, 'web/diskstat.html')


@login_required
def logStat(req):
    return render(req, 'web/logstat.html')


@login_required
def user(req):
    if req.user.is_superuser:
        return render(req, 'web/super_user.html')
    else:
        return render(req, 'web/user.html')


@login_required
def netStat(req, netname):
    netstat = NetworkStat.objects.values('name')
    name_list = []
    for name in netstat:
        name_list.append(name['name'])
    name = list(set(name_list))
    if not netname and name:
        netname = name[0]
    else:
        netname = netname
    return render(req, 'web/netstat.html', {"name": name, "netname": netname})


@login_required
def get_info(req, getname):
    if getname == 'cpu':
        cpu_stat = CpuStat.objects.all().order_by('add_time')
        data = []
        for each in cpu_stat:
            data.append([int(each.add_time), float(each.stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif getname == 'mem':
        mem_stat = MemStat.objects.all().order_by('add_time')
        data = []
        for each in mem_stat:
            data.append([int(each.add_time), float(each.stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif "on" in getname:
        netname = getname.split("_")[0]
        net_stat = NetworkStat.objects.filter(name=netname).order_by('add_time')
        data = []
        for each in net_stat:
            data.append([int(each.add_time), float(each.on_stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif "down" in getname:
        netname = getname.split("_")[0]
        net_stat = NetworkStat.objects.filter(name=netname).order_by('add_time')
        data = []
        for each in net_stat:
            data.append([int(each.add_time), float(each.down_stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif getname == 'loginfo':
        log_list, lenth = [], 0
        limit = req.GET.get("limit")
        offset = req.GET.get("offset")
        try:
            popen = Popen(r'ipmitool sel list', stdout=PIPE, stderr=PIPE, shell=True)
            info = popen.stdout.readlines()
            for msg in info:
                log_dict = {}
                data = msg.split('|')
                log_dict['id'] = data[0]
                log_dict['time'] = data[1] + data[2]
                if '/' in data[3]:
                    log_msg = data[3].split('/')
                    log_dict['name'] = log_msg[0]
                    log_dict['type'] = log_msg[1]
                else:
                    log_msg = data[3].split('#')
                    if len(log_msg) == 2:
                        log_dict['name'] = log_msg[1]
                        log_dict['type'] = log_msg[0]
                    else:
                        log_dict['name'] = log_dict['type'] = data[3]
                log_dict['desc'] = data[4] + '-' + data[5]
                log_list.append(log_dict)
            lenth = len(log_list)
            if not offset or not limit:
                log_list = log_list
            else:
                offset = int(offset)
                limit = int(limit)
                log_list = log_list[offset:offset + limit]
            if not log_list:
                raise Exception('error')
        except Exception as e:
            log_list = [{'id': 1, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'type': 'error',
                         'desc': 'no data', 'name': 'ipmi error'}]
            lenth = 1
            return HttpResponse(json.dumps({"rows": log_list, "total": lenth}))
        return HttpResponse(json.dumps({"rows": log_list, "total": lenth}))
    elif getname == "user":
        user = User.objects.all()
        lenth = len(user)
        user_list = []
        for each in user:
            list_dict = model_to_dict(each)
            list_dict.update({'last_login': each.last_login.strftime("%y-%m-%d %H:%M:%S")})
            list_dict.update({'date_joined': each.date_joined.strftime("%y-%m-%d %H:%M:%S")})
            user_list.append(list_dict)
        return HttpResponse(json.dumps({"rows": user_list, "total": lenth}))

