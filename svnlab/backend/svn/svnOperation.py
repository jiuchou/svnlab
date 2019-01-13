'''
user.svnOperation
~~~~~~~~~

This module implements the custom operation of LDAP server.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
'''

# built-in library

# third-party library
# 分页功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# user-defined
from .models import SvnList

# Create your views here.
def getSVNPathList(request):
    '''Get svn path list.
    '''
    response = {}
    try:
        req = request.GET

        # tmp = SvnList(name='b',dir_n=0,url='bbbb',number='bb',base_url='bbbbbb')
        # tmp.save()
        svnLists = SvnList.objects.filter(dir_n=req['dir_n']).values('name', 'dir_n', 'url', 'number', 'base_url')
        total = len(svnLists)

        svn_lists = []
        # Show 10 contacts per page
        paginator = Paginator(svnLists, 20)
        try:
            contacts = paginator.page(req['page'])
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        for svnList in contacts:
            svn_lists.append(svnList)

        response['data'] = {
            'total': total,
            'svn_lists': svn_lists
        }
        response['message'] = 'Success: get svn lists success!'
        response['status'] = 200
    except Exception as e:
        response['message'] = 'Failed: {}'.format(str(e))
        response['status'] = 500

    return JsonResponse(response)

def getDetailData(req):
    '''Get svn detail data.
    '''
    detailData = {}
    svnName = req['svnName']
    svnPath = req['svnPath']
    # token = req['token']
    # username = req['username']

    onlyReadUserNum = 0
    onlyReadUser = ''
    readAndWriteUserNum = 0
    readAndWriteUser = ''

    detailData = {
        "svnName": svnName,
        "svnPath": svnPath,
        "onlyReadUserNum": onlyReadUserNum,
        "onlyReadUser": onlyReadUser,
        "readAndWriteUserNum": readAndWriteUserNum,
        "readAndWriteUser": readAndWriteUser
    }
    return detailData

def getSVNPathDetail(request):
    '''Get svn detail.
    '''
    response = {}
    try:
        req = request.GET
        # 判断token，如果过期，报错，返回码401
        # 判断username，如果无权限，提示，返回码302

        detailData = getDetailData(req)
        if not detailData:
            response['message'] = 'Failed: get svn path detail failed, no access!'
            response['status'] = 302
            return JsonResponse(response)
        response['data'] = detailData
        response['message'] = 'Success: get svn path detail success!'
        response['status'] = 200
    except Exception as e:
        response['message'] = 'Failed: get svn path detail failed, server error! {}'.format(e)
        response['status'] = 500
    return JsonResponse(response)
