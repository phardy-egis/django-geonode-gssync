from django.urls import path
from . import views

urlpatterns = [
    # Main templage
    path('', views.SyncHomePage.as_view(), name='gssync_index'),
    # Get task progress
    path('api/tasks/<str:task_id>/', views.GeoserverSyncProgressView.as_view(), name='gssync_sync'),
    # Run sync task
    path('api/sync/', views.GeoserverSyncView.as_view(), name='gssync_progress'),
]

