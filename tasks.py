
from celery import current_task
from geonode.celery_app import app
from .helpers.sync import sync_dataset_from_geoserver 
    
@app.task(
    bind=True,
    queue="geonode.gssync",
    expires=30,
    time_limit=600,
    acks_late=False,
    ignore_result=False
)
def sync_dataset_from_geoserver_task(self, user_id, json_payload):
    created_dataset_pk = sync_dataset_from_geoserver(user_id, **json_payload)
    return created_dataset_pk