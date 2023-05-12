
from celery import current_task
from geonode.celery_app import app
from geonode.geoserver.tasks import geoserver_update_datasets
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

@app.task(
    name='geonode.gssync.tasks.gssync_task',
    queue='default',
)
#def gssync_task(layerfilter):
def gssync_task(owner=None, filter=None):
    # Updating task state
    current_task.update_state(state='PROGRESS')

    # Getting owner profile
    profile = get_object_or_404(get_user_model(), Q(is_active=True), username=owner)

    # Starting heavy operation
    output = geoserver_update_datasets(owner=profile, filter=filter, ignore_errors=False, skip_geonode_registered=True)

    # Updating task state
    current_task.update_state(state='SUCCESS', meta={"result": output, "input":{
        "owner":owner,
        "filter":filter,
    }})