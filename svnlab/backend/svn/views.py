'''
svn.views
~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
'''

# built-in library
import time

# third-party library
from django.http import JsonResponse

# user-defined
from .models import Report

# Create your views here.
def changeUserRole(request):
    '''View of user login operation.
    '''
    response = {}
    try:
        req = request.GET
        username = req['username']
        applicant = req['username']
        path = req['path']
        oldRole = req['oldRole']
        newRole = req['newRole']

        identifierTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        identifier = 'svnlab{}'.format(identifierTime)
        applySource = 'PermissionManagement-User'

        if Report.objects.filter(username=username, path=path, state=0):
            response['message'] = 'Forbidden: change role by user failed! username: {}'.format(username)
            response['status'] = 403
        else:
            Report.objects.create(
                identifier=identifier,
                path=path,
                username=username,
                applicant=applicant,
                old_role=oldRole,
                new_role=newRole,
                state=0,
                apply_source=applySource
            )
            response['message'] = 'Success: change role by user success! username: {}'.format(username)
            response['status'] = 200
    except Exception as e:
        response['message'] = 'Failed: {}'.format(str(e))
        response['status'] = 500

    return JsonResponse(response)
