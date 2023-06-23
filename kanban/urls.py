from django.urls import path

from . import views

app_name = 'kanban'

urlpatterns = [
    path('board/', views.board, name='board'),
    
    path('create_project/', views.create_project, name='create_project'),
    path('project_detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('project_list/', views.project_list, name='project_list'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),

    path('create_task/', views.create_task, name='create_task'),
    path('get_assigned_users/<int:project_id>/', views.get_assigned_users, name='get_assigned_users'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
    path('tasks/', views.task_list, name='task_list'),
    path('task_detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
]