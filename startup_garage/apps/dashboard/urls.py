from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('profile/update/', views.StartupProfileUpdateView.as_view(), name='profile_update'),
]

