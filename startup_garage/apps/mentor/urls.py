from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('', views.mentor_list, name='list'),
    path('<int:pk>/', views.mentor_detail, name='detail'),
    
    # Feedback URLs
    path('create/', views.FeedbackCreateView.as_view(), name='feedback-create'),  # Shortcut
    path('feedback/', views.FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/create/', views.FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback/<int:pk>/edit/', views.FeedbackUpdateView.as_view(), name='feedback-update'),
    path('feedback/<int:pk>/complete/', views.complete_next_step, name='feedback-complete'),
]
