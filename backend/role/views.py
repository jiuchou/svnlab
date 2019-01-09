from django.http import JsonResponse
from backend.role.models import Role
#分页功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def getPermissionList(request):
    response = {}
    try:
        req = request.GET
        username = req['username']
        page = req['page']

        roleList = Role.objects.filter(username=username).values('username', 'path', 'module', 'manager', 'role').order_by('path')
        print(roleList)
        total = len(roleList)

        roleListByPaginator = []
        # show 10 contacts per page
        paginator = Paginator(roleList, 20)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of resluts.
            contacts = paginator.page(paginator.num_pages)
        for role in contacts:
            roleListByPaginator.append(role)

        response['data'] = {
            'total': total,
            'roleList': roleListByPaginator
        }
        response['message'] = 'Success: get role lists success!'
        response['status'] = 200
    except Exception as e:
        response['message'] = 'Failed: {}'.format(str(e))
        response['status'] = 500

    return JsonResponse(response)
