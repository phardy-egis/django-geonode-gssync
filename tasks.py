
from celery import current_task
from geonode.celery_app import app
from django.core import management
import subprocess

@app.task(
    name='geonode.gssync.tasks.gssync_task',
    queue='default',
)
#def gssync_task(layerfilter):
def gssync_task():
    # Updating task state
    current_task.update_state(state='PROGRESS', meta={})
    # filter = '--filter='+str(layerfilter)
    # Running task
    # if layerfilter != '':
    #     management.call_command('updatelayers', '--skip-geonode-registered', filter)
    # else:
    management.call_command('updatelayers')
    # Updating task state
    current_task.update_state(state='SUCCESS', meta={})