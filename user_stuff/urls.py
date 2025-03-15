from django.urls import path
from .views import (
    UserPreferenceCreateView,
    UserPreferenceListView,
    NotificationCreateView,
    NotificationListView,
    MonthlyPerformanceView,
    AssetPerformanceView,
)

urlpatterns = [
    path('user_preference/', UserPreferenceCreateView.as_view(), name='user_preference_create'),
    path('user_preferences/', UserPreferenceListView.as_view(), name='user_preference_list'),
    path('notifications/', NotificationCreateView.as_view(), name='notification_create'),
    path('notifications/list/', NotificationListView.as_view(), name='notification_list'),
    path('monthly_performance/', MonthlyPerformanceView.as_view(), name='monthly_performance'),
    path('asset_performance/', AssetPerformanceView.as_view(), name='asset_performance'),
]