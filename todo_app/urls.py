from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('', login_required(views.task_list), name='task_list'),
    path('task/<int:task_id>/', login_required(views.task_detail), name='task_detail'),
    path('task/add/', login_required(views.add_task), name='add_task'),
    path('task/<int:task_id>/delete/', login_required(views.delete_task), name='delete_task'),
    path('progress/', login_required(views.progress), name='progress'),
    path('reports/', login_required(views.reports), name='reports'),
]
