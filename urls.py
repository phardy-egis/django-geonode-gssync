from django.urls import path
from . import views

urlpatterns = [
    # Main templage
    path('', views.index, name='start_task'),
    # Task startup
    path('api/tasks/start/', views.start_task, name='start_task'),
    # Get task progress
    path('api/tasks/<str:task_id>/', views.get_task, name='get_task'),
]

