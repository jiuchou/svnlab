"""
user.module_permission
~~~~~~~~~~~~~~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.04.08
"""
import json
import os
import re

from django.core.paginator  import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse

from svnlab.common.decorator import get_username
from .models import Permission

def get_subpaths(module,path):
    subpaths = []

    filename = "authfilename"
    with open(filename,'r') as f:
        text = f.read()
    # import re
    # text = open('zz','r').read()
    # regex = r"[{0}:/{1}.*".format(module,path)
    path_infos = re.findall(regex, text)
    for path_info in path_infos:
        subpath = path_info.strip('/').strip('[')
        subpaths.append(subpath)

    return subpaths

def get_url(module,path):
    """Get url.

    Get url by module and path.
    """
    url = ""

    filename = "module_preurl_map"
    with open(filename, 'r') as f:
        text = f.read()
    regex = "{0}(.*)".format(module)
    preurl = re.findall(regex, text)[0].strip(',').strip('/')
    url = "{0}/{1}/{2}".format(preurl,module,path)

    return url

def get_reader_and_writer(module,path)
    """Get owner.

    Get owner by url from manageToUrl
    """
    reader=""
    writer=""

    filename="authfilename"
    with open(filename,'r') as f:
        text=f.read()
    #import re
    #text=open("zz','r').read()
    #regex = r"[Documents:/IVSDocs/智能算法部/TDT/技术预研项目/DH3.RD002064_基础算法部预研]
    regex = r"[{0}:/{1}]".format(module,path)
    permission_list = text.split(regex)[1].split('[')[0].strip().split('\n')
    for permission in permission_list:
        if "=rw" in permission:
            reader = reader + permission.split("=")[0]
        else:
            writer = writer + permission.split("=")[0]

    resder = reader.strip(",")
    writer = writer.strip(",")

    return reader,writer

def get_owner(url):
    """Get owner.

    Get owner by url form manageToUrl
    """
    owner = ""

    filename = "owner_url_map"
    with open(filename, 'r') as f:
        text = f.read()
    regex = "(.*){0}\n".format(url)
    owner = re.findall(regex,text)[0].strip(',')

    return owner

def update_permission_list(module,path):
    try:
        url = get_url(module,path)
        owner = get_owner(url)
        reader,writer = get_reader_and_writer(module,path)

        if Permission.objects.filter(url=url):
            permission.objects.filter(url=url).update(module=module,
                                                      path=path,
                                                      url=url,
                                                      owner=owner,
                                                      reader=reader,
                                                      writer=writer,
                                                      reader_number=reader_number,
                                                      writer_number=writer_number)
            print("INFO:Update module permission list successfull")
        else:
            Permission.objects.create(module=module,
                                      path=path,
                                      url=url,
                                      owner=owner,
                                      reader=reader,
                                      writer=writer,
                                      reader_number=reader_number,
                                      writer_number=writer_number)
            print(INFO:Create module permission list successfull")
    except Exception as e:
        print(e)

def update_module_permission_list(request):
    """Update _module_permission_list info.

    update_module_permission_list info to PERMISSION_LIST that was the name 
    of database table. Permission list container:
        [module, path, reader, writer, owner]

     Args:
        module: module name 
         path: path name

    Returns:
        None 

    Raises:
    """
    pass
    reaponse= {}
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)

    try:
        username = get_username(token)
        req = request.GET
        module = req['module']
        path = req['path']

        subpaths = get_subpaths(module, path)
        for subpath in subpaths:
            update_permission_list(module, subpath)
    except Exception as e:
        response['message'] = "ERROR: Writer database report status failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    response['message]= "SUCCESS:Change role by user success!"
    reaponse['status_code'] = 200
    return JsonResponse(reaponse)

def get_module_permission_list(request):
    response ={}
    token = request.META.get('HTTP_AUTHORIZATION')

    try:
        username = get_username(token)
        req = request.Get
        page = req['page']
        limit = req['limit']

        permission = Permission.objects.filter(owner=username)\
                            .values("owner",
                                    "module",
                                    "path",
                                    "url",
                                    "reader",
                                    "writer",
                                    "reader_number",
                                    "writer_number").order_by("url")
        response['total'] = len(permissions)

        permission_list = []
        paginator = Paginator(permissions,limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            #If page is out of range (e.g.9999), deliver last page of resluts.
            contacts = pageinator.page.(paginator,num_pages)

        for permission in contacts:
            permission_list.append(permission)

        response['permission_list'] = permission_list
        response['message'] = "SUCCESS:Get module permission list successfull"
        response['status_code']= 200
    except Exception as e:
        response['message'] = "ERROR: Verify authentication failed! {0}".format(e)
        response[/status_code'] = 401
        return JsonResponse(response)
    return JsonResponse(response)

def refresh_module_permission_detail():
    pass
