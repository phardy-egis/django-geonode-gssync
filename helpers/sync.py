from geonode.layers.models import Dataset
from geonode.resource.manager import resource_manager
import uuid

def sync_dataset_from_geoserver(user_profile, layer_alternate, layer_title, viewer_group, manager_group):  
    layer = resource_manager.create(
        str(uuid.uuid4()),
        resource_type=Dataset,
        defaults=dict(
            name=layer_alternate.split(':')[1],
            workspace=layer_alternate.split(':')[0],
            store='geonode_data',
            subtype='vector',
            alternate=layer_alternate,
            title=layer_title,
            abstract="Test import manuel",
            owner=user_profile,
        ),
    )
    perm_spec = {
        'users': {
            'super_admin': [
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
        'groups': {
            '{}'.format(viewer_group) : [
                'view_resourcebase'
            ],
            '{}'.format(manager_group): [
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
        }
    }
    resource_manager.set_permissions(layer.uuid, permissions=perm_spec)
    resource_manager.update(layer.uuid, instance=layer, notify=False)

# from django.contrib.auth import get_user_model
# user_profile = get_user_model().objects.filter(username='super_admin').first()    
# sync_dataset_from_geoserver(
#     user_profile,
#     'geonode:7081f88e-dc07-461d-bce6-6c6f709e3b8b_0x66a27b03',
#     'Critère prétraité',
#     'gmva-utilisateurs-mca',
#     'gmva-administrateurs-mca'
# )