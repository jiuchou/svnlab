'''
svn.views
~~~~~~~~~

This module implements the Requests Views.
View is an logical management library, written in Python, for user beings.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.03.27
'''
import json
import os
import time

from django.http import JsonResponse

from .models import Report
from backend.user.models import UserRole
from svnlab.common.decorator import get_username

def update_role(request):
    """Update role
    """
    response = {}
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    identifier = 'svnlab{}'.format(timestamp)
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        applicant = get_username(token)
    except Exception as e:
        response['message'] = "ERROR: Verify authentication failed! {0}".format(e)
        response['status_code'] = 401
        return JsonResponse(response)

    req = json.loads(request.body.decode())
    print(req)
    path = req['path']
    module = req['module']
    username = req['username']
    old_role = req['old_role']
    new_role = req['new_role']

    try:
        if Report.objects.filter(username=username,
                                 path=path,
                                 module=module,
                                 status=0):
            print("WARNING: username({0}) is running".format(username))
        else:
            Report.objects.create(
                identifier=identifier,
                path=path,
                username=username,
                applicant=applicant,
                old_role=oldRole,
                new_role=newRole,
                status=0,
                apply_source=applySource
            )
    except Exception:
        response['message'] = "ERROR: Write database report status failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    # Update role
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    authfile = "{0}/common/roleUtils/dav_svn.authz".format(BASE_DIR)
    cmd = "bash {0}/common/utils/update_authfile.sh {1} {2} {3} {4} {5}".format(
        BASE_DIR,
        authfile,
        module,
        path,
        username,
        new_role
    )
    print(cmd)
    result = os.system(cmd)

    # Update database
    try:
        if result == 0:
            Report.objects.filter(username=username,
                                  path=path,
                                  module=module,
                                  status=0).update(status=1)
            UserRole.objects.filter(username=username,
                                    path=path,
                                    module=module).update(role=new_role)
        else:
            Report.objects.filter(username=username,
                                  path=path,
                                  module=module,
                                  status=0).update(status=2)
    except Exception:
        response['message'] = "ERROR: Write database report status failed!"
        response['status_code'] = 500
        return JsonResponse(response)

    response['message'] = "SUCCESS: Change role by user success!"
    response['status_code'] = 200
    return JsonResponse(response)
