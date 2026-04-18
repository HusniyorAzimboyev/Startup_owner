from django.urls import path
from . import views

app_name = 'investor'

urlpatterns = [
    path('', views.investor_list, name='list'),
    path('<int:pk>/', views.investor_detail, name='detail'),
    
    # Dashboard
    path('dashboard/', views.InvestorDashboardView.as_view(), name='dashboard'),
    
    # Meetings
    path('meeting/create/', views.MeetingCreateView.as_view(), name='meeting-create'),
    path('meeting/<int:pk>/edit/', views.MeetingUpdateView.as_view(), name='meeting-update'),
    path('meeting/<int:pk>/delete/', views.MeetingDeleteView.as_view(), name='meeting-delete'),
    
    # Pitch Deck
    path('pitch-deck/edit/', views.PitchDeckUpdateView.as_view(), name='pitchdeck-update'),
]
