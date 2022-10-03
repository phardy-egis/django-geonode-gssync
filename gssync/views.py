# Web
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404

# Management commands
from django.core.management import call_command

# Celery results
from .tasks import gssync_task
from celery.result import AsyncResult

# This wiew render template that call the endpoints
def index(request):
    # Only users with admin permissions have access to this view
    if request.user.is_superuser:
        context={}
        return render(request, 'gssync/index.html', context)

    # Non-admin are redirected to 404
    else:
        raise Http404("This page does not exists")

# (JSON endpoint) This wiew start the sync between geonode and geoserver
def start_task(request):
    # Only users with admin permissions have access to this view
    if request.user.is_superuser:
        # Starting celery task
        task = gssync_task.delay()
        response_data = {
            'task_id': task.task_id,
            'task_url': '/gssync/api/tasks/{task_id}/'.format(task_id=task.task_id)
        }
        return JsonResponse(response_data)
    
    # Non-admin are redirected to 404
    else:
        raise Http404("This page does not exists")

# (JSON endpoint) This wiew retrieve information regarding task progress
def get_task(request, task_id):
    # Only users with admin permissions have access to this view
    if request.user.is_superuser:
        #fetching progress of task and returning it in JSON format
        result = AsyncResult(task_id)
        response_data = {
            'state': result.state,
            'details': result.info,
        }
        return JsonResponse(response_data)

    # Non-admin are redirected to 404
    else:
        raise Http404("This page does not exists")