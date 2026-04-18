from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressOverviewView.as_view(), name='overview'),
    path('dashboard/', views.progress_dashboard, name='dashboard'),
    path('metrics/', views.metrics_detail, name='metrics'),
]
