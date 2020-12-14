from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('scooters', views.scooters_list_view),
    path('scooters/new/', views.create_new_scooter_view),
    path('scooters/redact/<str:scooter_id>/', views.redact_scooter_view),
    path('scooters/<str:scooter_id>/', views.scooter_card_view),
    path('clients', views.client_list_view),
    path('clients/<str:client_id>/', views.client_card_view),
    path('alerts', views.alerts_list_view),
    path('alerts/settings/', views.alert_settings_view),
    path('alerts/<str:alert_id>/', views.alert_card_view),
    path('', views.dashboard)
]
