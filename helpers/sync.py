from geonode.layers.models import Dataset
from geonode.resource.manager import resource_manager
from django.contrib.auth import get_user_model
from geonode.utils import OGC_Servers_Handler
from geonode import settings
from geoserver.catalog import Catalog
import uuid

def sync_dataset_from_geoserver(user_id, geoserver_layer_name, geoserver_layer_workspace='geonode', geoserver_layer_store='geonode_data', viewer_groups=[], manager_groups=[], geonode_dataset_abstract='Automatically synced from geoserver.', geonode_dataset_title=None, geoserver_layer_type='vector'):  
    """This functions takes a geoserver layer as input and sync it with geonode catalog.

    Args:
        user_id (int): Django User ID used to set dataset owner
        geoserver_layer_name (str): Name of geoserver layer
        geoserver_layer_workspace (str, optional): Name of geoserver workspace containing geoserver layer to sync. Defaults to 'geonode'.
        geoserver_layer_store (str, optional): Name of geoserver layer store containing geoserver layer to sync
        viewer_group (array, optional): Name of group that must benefit viewing permissions. Defaults to [].
        manager_group (array, optional): Name of group that must benefit managing permissions. Defaults to [].
        geonode_dataset_abstract (str, optional): Content of layer abstract stored in geonode. Defaults to 'Automatically synced from geoserver.'.
        geonode_dataset_title (str, optional): Title of layer stored in geonode. Defaults to None.
        geoserver_layer_type (str, optional): Type of layer (vector/raster). Defaults to 'vector'.
    """
    # Checking that layer exists in geoserver catalog
    ogc_server_settings = OGC_Servers_Handler(settings.OGC_SERVER)["default"]
    url = ogc_server_settings.rest
    _user, _password = ogc_server_settings.credentials
    gs_catalog = Catalog(
        url, _user, _password, retries=ogc_server_settings.MAX_RETRIES, backoff_factor=ogc_server_settings.BACKOFF_FACTOR
    )
    geoserver_layers = gs_catalog.get_layers()
    layer_checked = False
    for geoserver_layer in geoserver_layers:
        if f'{geoserver_layer_workspace}:{geoserver_layer_name}' == geoserver_layer.name:
            layer_checked = True
            print(geoserver_layer.name)
            break

    if not layer_checked:
        raise Exception("Layer does not exists in geoserver.")
    
    Profile = get_user_model()
    user_profile = Profile.objects.get(id=user_id)
    
    if not geonode_dataset_title:
        geonode_dataset_title = geoserver_layer_name
       
    layer = resource_manager.create(
        str(uuid.uuid4()),
        resource_type=Dataset,
        defaults=dict(
            name=geoserver_layer_name,
            workspace=geoserver_layer_workspace,
            store=geoserver_layer_store,
            subtype=geoserver_layer_type,
            alternate=f'{geoserver_layer_workspace}:{geoserver_layer_name}',
            title=geonode_dataset_title,
            abstract=geonode_dataset_abstract,
            owner=user_profile,
        ),
    )
    
    # Setting permissions for dataset
    perm_spec = {
        'users': {
            '{username}'.format(username=user_profile.username): [
                'publish_resourcebase',
                'change_dataset_style',
                'change_resourcebase',
                'download_resourcebase',
                'change_resourcebase_metadata',
                'change_resourcebase_permissions',
                'view_resourcebase',
                'delete_resourcebase',
                'change_dataset_data'
            ]
        }, 
        'groups': {}
    }
    for viewer_group in viewer_groups:
        perm_spec['groups']['{}'.format(viewer_group)] = [
            'view_resourcebase'
        ],
    
    for manager_group in manager_groups:
        perm_spec['groups']['{}'.format(manager_group)] = [
            'publish_resourcebase',
            'change_dataset_style',
            'change_resourcebase',
            'download_resourcebase',
            'change_resourcebase_metadata',
            'change_resourcebase_permissions',
            'view_resourcebase',
            'delete_resourcebase',
            'change_dataset_data'
        ]
    resource_manager.set_permissions(layer.uuid, permissions=perm_spec)
    
    # Update geofence rules for geoserver
    resource_manager.update(layer.uuid, instance=layer, notify=False)
    
    return layer.pk

# from django.contrib.auth import get_user_model
# user_profile = get_user_model().objects.filter(username='super_admin').first()    
# sync_dataset_from_geoserver(
#     user_profile,
#     'geonode:7081f88e-dc07-461d-bce6-6c6f709e3b8b_0x66a27b03',
#     'Critère prétraité',
#     'gmva-utilisateurs-mca',
#     'gmva-administrateurs-mca'
# )