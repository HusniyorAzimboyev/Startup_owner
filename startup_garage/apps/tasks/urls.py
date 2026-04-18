from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskBoardView.as_view(), name='task-board'),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/move/', views.task_move, name='task-move'),
]

