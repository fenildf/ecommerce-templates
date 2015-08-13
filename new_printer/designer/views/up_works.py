#!/usr/bin/env python
# encoding: utf-8
# *-* coding: utf-8 -*-
'''
* data: 2015-8-10 8:17
  use: designer's personal
'''
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json, os, uuid, base64, platform, requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from designer.conf import website 
from configuration.models import Goods_Upload
from django.contrib.auth.models import User
import httplib, urllib
import urllib2,os
from datetime import date ,datetime
import time
import json,pdb


def index(request):
    return render(request, website.index)

def stls_save(stls):
    jwary_md5 = {}
    file_size = []
    has_existed = {}
    count = 0
    for stl in stls:
        #pdb.set_trace()         
        stl_type=str(stl)
        stl_type=stl_type.split('.')
        stl_md5 = file_save(stl,stl_type[0],stl_type[1])
        #jwary_md5.setdefault(stl_type[0],stl_md5)
        size = len(stl)
        file_size.append(size)
        stl_type=str(stl)
        stl_type=stl_type.split('.')
        stl_md5 = file_save(stl,stl_type[0],stl_type[1])
        stl_path = str(stl_md5) + '.stl'
        if not Goods_Upload.objects.filter(stl_path=stl_path).exists():
            jwary_md5.setdefault(stl_type[0],stl_md5)
        else:
            has_existed.setdefault(stl_type[0],stl_md5)
    for md5 in jwary_md5:
        stl_url = str(jwary_md5[md5])+'.stl'
        tags = 'Jweary'
        new_jwary = Goods_Upload.objects.create(goods_name = str(md5),
                                         designer_id = 1,
                                         stl_path = str(stl_url),
                                         tags = tags,
                                         file_size = str(float('%0.3f'%(file_size[count]/1024.0/1024.0)))+'M',
                                         good_state = 0
                                        )
        count = count + 1
    print has_existed
    return has_existed
#@login_required
def works_save(request):
    #pdb.set_trace()
    if request.method == 'POST':
        a_have = True
        jwary_stl = request.FILES.getlist('jiezhi')
        drop_stl = request.FILES.getlist('2')
        #eardrop_stl = request.FILES.getlist('3')
        #twist_stl = request.FILES.getlist('4')
        #necklace_stl = request.FILES.getlist('5')
        ##needle_stl = request.FILES.getlist('6')
        file_hased = []
        #ids = []
        #pdb.set_trace()
        count = 0
        if jwary_stl:
            existed = stls_save(jwary_stl)
            if existed:
                for i in existed:
                    conf = {'hased':i}
                    file_hased.append(conf)
        if drop_stl:
            stls_save(drop_stl)
        return HttpResponse(json.dumps(file_hased))
    else:
        return render(request, website.up_error)


def file_save(model,name,stl_type):
    #pdb.set_trace()
    chunks = ""
    for chunk in model.chunks():
        chunks = chunks + chunk
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'style')
    data.append(stl_type)
    #data.append('Content-Disposition: form-data; name="%s"\r\n' % 'this_id')
    #data.append(this_id)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('profile',str(name)))
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(chunks)
    data.append('--%s--\r\n' % boundary)
    http_url = website.toy_server_upload#'http://192.168.1.104:8888/file/upload'
    http_body = '\r\n'.join(data)
    req = urllib2.Request(http_url, data=http_body)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_header('User-Agent','Mozilla/5.0')
    req.add_header('Referer','%s'%website.toy_server_ip)#'http://192.168.1.104:8888/')
    resp = urllib2.urlopen(req, timeout=2545)
    qrcont=resp.read()
    md = json.loads(qrcont)
    md5 = md['status']
    return md5


def workd_execute(request):
    user = request.user
    designer = Designer.objects.get(user_id=user.id)
    designer.icon = str(website.icon_server_path) + designer.icon
    unpass_list = Goods_Upload.objects.filter(customer_id=customer.id)
    conf = {'all_list':unpass_list,
            'icon' : designer.icon,
            'name':designer.name,
              }
    return render(request, website.all_list, conf)

def delete(request):
    ids = request.POST['ids']
    for id in ids:
        Goods_Upload.objects.remove(id = id)
    conf = {'status':"success"}
    return HttpResponse(json.dumps(conf))

def photo_edit(request):
    id = request.POST['id']
    photo = Goods_Upload.objects.filter(id=id)
    conf = {'photo':'photo'}
    return HttpResponse(json.dumps(conf))

#未处理页面，点击处理并提交 的处理表单；同时也是 未通过，点击重生申请发布的 处理表单
def edit_submit(request):

    #file_id = request.POST['id']
    file_id = 23
    count = 1
    p_url = []
    #pdb.set_trace()
    photo = Goods_Upload.objects.get(id=file_id)
    stl_md5 = photo.stl_path
    print stl_md5
    stl_md5 = str(stl_md5).split('.')
    
    stl_md5 = stl_md5[0]
    price = request.POST['price']
    #previews = request.FILES.getlist['photo']
    previews = request.FILES['photo']
    describe = request.POST['describe']
    #name = request.POST['edit_name']
    '''if not name:
        name = photo.name'''
    if previews:
        #for preview_one in previews:
        preview_type=str(previews)
        preview_type=preview_type.split('.')
        preview_md5 = photo_save(previews,preview_type[0],preview_type[1],stl_md5)
        p1_url = str(preview_md5)+'.'+str(preview_type[1])
        p_url.append(p1_url)

    s=Goods_Upload.objects.filter(id= file_id).update(#name=str(name),
                        goods_price = int(price),
                        preview_1 = p_url[0],
                        #preview_2 = p_url[1],
                        #preview_3 = p_url[2],
                        description = describe
                      )
    conf = {'status':"success"}
    return HttpResponse(json.dumps(conf))
    '''else:
        s=Goods_Uploadobjects.filter(id= id).update(name=str(name),
                        price = int(price),
                        describe = describe
                      )
        conf = {'status':"success"}
        return HttpResponse(json.dumps(conf))'''
def photo_save(model,name,stl_type,stl_md5):
    #pdb.set_trace()
    chunks = ""
    for chunk in model.chunks():
        chunks = chunks + chunk
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'style')
    data.append(stl_type)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'md5')
    data.append(stl_md5)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('profile',str(name)))
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(chunks)
    data.append('--%s--\r\n' % boundary)
    http_url = 'http://192.168.1.116:8888/file/imgupload'
    http_body = '\r\n'.join(data)
    req = urllib2.Request(http_url, data=http_body)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_header('User-Agent','Mozilla/5.0')
    req.add_header('Referer','%s'%website.toy_server_ip)#'http://192.168.1.104:8888/')
    resp = urllib2.urlopen(req, timeout=2545)
    qrcont=resp.read()
    md = json.loads(qrcont)
    print md
    md5 = md['status']
    print md5
    return md5

#未通过页面，点击重新申请发布
def photo_not_passed(request):#未通过页面，点击重新申请发布
    id = request.POST['id']
    photo = Goods_Upload.objects.filter(id=id)
    conf = {'photo':'photo'}
    return HttpResponse(json.dumps(conf))





def auditing(request):#审核中
    user = request.user
    designer = Designer.objects.get(user_id=user.id)
    photo = Goods_Upload.objects.filter(design_id=design.id)
    conf = {'photo':'photo'}
    return HttpResponse(json.dumps(conf))


def has_published(request):#显示已发布页面
    user = request.user
    designer = Designer.objects.get(user_id=user.id)
    photo = Goods.objects.filter(design_id=design.id)
    conf = {'photo':'photo'}
    return HttpResponse(json.dumps(conf))
def published_edit(request):#在已发布页面点击编辑后，传的值
    id = request.POST['id']
    photo = Goods.objects.get(id=id)
    conf = {'photo':'photo'}
    return HttpResponse(json.dumps(conf))


def published_submit(request):#在已发布页面点击编辑后，修改后提交的值
    file_id = request.POST['id']
    photo = Goods_Upload.objects.filter(id=file_id)
    price = request.POST['price']
    describe = request.POST['describe']
    name = request.POST['name']
    if not name:
        name = photo.name
    if not describe:
        describe = photo.describe
    if not price:
        price = photo.price
    s=Goods_Uploadobjects.filter(id= id).update(name=str(name),
                        price = int(price),
                        describe = describe
                      )
    conf = {'status':"success"}
    return HttpResponse(json.dumps(conf))

def published_delete(request):#在已发布页面点击编辑后，点击删除
    pass

