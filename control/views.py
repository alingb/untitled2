# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from detail.salt import SaltApi
# Create your views here.


@login_required
def index(req):
    if req.POST:
        info = eval(req.POST.get("data"))
        name = info["ip"]
        cmd = info["cmd"]
        salt_api = "https://192.168.1.57:8000/"
        salt = SaltApi(salt_api)
        salt_client = name[0]
        salt_test = 'test.ping'
        salt_method = 'cmd.run'
        salt_params = cmd
        result1 = salt.salt_command(salt_client, salt_test)
        print result1
        result2 = salt.salt_command(salt_client, salt_method, salt_params)
        print result2
        lenth = 2
        data = [{"server": "master", "data": "sucess"}, {"server": "slaver03", "data": "sucess"}]
        return HttpResponse(json.dumps([{"data": result2, "server": "master"}]))
    elif req.GET:
        lenth = 2
        data = [{"server": "master", "data": "sucess"}, {"server": "slaver03", "data": "sucess"}]
        return HttpResponse(json.dumps({"rows": data, "total": lenth}))
    else:
        name = {"master": "master", "slave2": "slave2"}
        return render(req, "control/index.html", {'name': name})


def ret_show(request):
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    lenth = 2
    data = [{"server": "master", "data": "sucess"}, {"server": "slaver03", "data": "fail"}]
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))

