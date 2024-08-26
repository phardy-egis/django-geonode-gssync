# Django template view
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Celery results
from celery.result import AsyncResult

# Django REST ApiView requirements
import json
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .tasks import sync_dataset_from_geoserver_task
from rest_framework.exceptions import ParseError

# 
class SyncHomePage(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """This view render the template that allow user to trigger syncing geoserver layer into geonode.

    Args:
        LoginRequiredMixin (_type_): This mixin enforce user to be authenticated to access this endpoint
        UserPassesTestMixin (_type_): This mixin enforces users to be authenticated to access this endpoint
        TemplateView (_type_): This mixim enforces users to be authenticated to access tthis endpoint
    """
    template_name = 'gssync/index.html'
    
    def test_func(self):
        """This view test if user is admin for UserPassesTestMixin

        Returns:
            boolean: True if user is is_superuser
        """
        return self.request.user.is_superuser

class GeoserverSyncView(APIView):
    """This view allow to make dataset available in Geonode from a layer previously added in Geoserver.
    The owner of the dataset will be the user triggering the POST request.
    
    To use this endpoint:
    
    * User must be authenticated
    * User must be admin
    
    The payload must be sent with `application/json` header. The request payload required is defined below:
    
    ```json
    {
        "geoserver_layer_name":"GEOSERVER_LAYER_NAME",
        "geoserver_layer_workspace":"geonode",
        "geoserver_layer_store":"geonode_data",
        "viewer_groups":["viewer-group-slug-1", "viewer-group-slug-2"],
        "manager_groups":["manager-group-slug-1", "manager-group-slug-2"],
        "geonode_dataset_abstract":"TYPE HERE AN ABSTRACT",
        "geonode_dataset_title":"TYPE HERE LAYER TITLE DISPLAYED IN GEONODE",
        "geoserver_layer_type":"TYPE HERE LAYER TYPE DISPLAYED IN GEONODE"
    }
    ```
    The details of parameters added in the JSON above is listed below. 
    Optional parameters should not be part of JSON sent if not used.
    
    - Mandatory parameters:
    
        - `geoserver_layer_name` (str): Name of geoserver layer
    
    - Optional parameters:
        
        - `geoserver_layer_workspace` (str, optional): Name of geoserver workspace containing geoserver layer to sync. Defaults to 'geonode'.
        - `geoserver_layer_store` (str, optional): Name of geoserver layer store containing geoserver layer to sync. Defaults to 'geonode_data'.
        - `viewer_group` (array, optional): Slug list of Geonode user groups that must have viewing permissions set on dataset imported. Defaults to [].
        - `manager_group` (array, optional): Slug list of Geonode user groups that must have managing permissions set on dataset imported. Defaults to [].
        - `geonode_dataset_abstract` (str, optional): Content of layer abstract stored in geonode. Defaults to 'Automatically synced from geoserver.'.
        - `geonode_dataset_title` (str, optional): Title of layer stored in geonode. Defaults to None.
        - `geoserver_layer_type` (str, optional): Type of layer (vector/raster). Defaults to 'vector'.
    
    """
    
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        
        user_id = request.user.id
        
        try:
            task = sync_dataset_from_geoserver_task.delay(user_id, request.data)
            response_data = {
                'task_id': task.task_id,
                'task_url': '/gssync/api/tasks/{task_id}/'.format(task_id=task.task_id)
            }
            return Response(response_data)
        except Exception as e:
            raise ParseError(f'Error syncing dataset. The process returned the following error: {e}')

# (JSON endpoint) This wiew retrieve information regarding task progress
class GeoserverSyncProgressView(APIView):
    
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    
    def get(self, request, task_id):
        #fetching progress of task and returning it in JSON format
        current_task = AsyncResult(task_id)
        result = {
            "task_id": current_task.task_id,
            "task_status": current_task.status,
            "geonode_layer_id": current_task.get()
        }
        return Response(result)