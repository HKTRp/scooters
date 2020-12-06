from django.urls import path
from . import views

urlpatterns = [

    path('getScooter/', views.GetScooterView.as_view(), name='get_scooters'),
    path('addScooter/', views.AddScooterView.as_view(), name='add_scooter'),
    path('changeScooterStatus/', views.ChangeScooterStatusView.as_view(), name='change_scooter_status'),
    path('addScooterToGroup/', views.AddScooterToGroupView.as_view(), name='add_scooter_to_group'),
    path('removeScooterFromGroup/', views.RemoveScooterFromGroupView.as_view(), name='remove_scooter_from_group'),
    path('removeScooter/', views.RemoveScooterView.as_view(), name='remove_scooter'),
    path('changeScooter/', views.ChangeScooterDataView.as_view(), name='change_scooter'),

    path('getScootersGroup/', views.GetScootersGroupView.as_view(), name='get_scooters_group'),
    path('addScooterGroup/', views.AddScootersGroupView.as_view(), name='add_scooter_group'),
    path('removeScooterGroup/', views.RemoveScootersGroupView.as_view(), name='remove_scooter_group'),

    path('getClient/', views.GetClientView.as_view(), name='get_clients'),
    path('addClient/', views.AddClientView.as_view(), name='add_client'),
    path('addClientToGroup/', views.AddClientToGroupView.as_view(), name='add_client_to_group'),
    path('removeClientFromGroup/', views.RemoveClientFromGroupView.as_view(), name='remove_client_from_view'),
    path('changeClientStatus/', views.ChangeClientStatusView.as_view(), name='change_client_status'),
    path('ClientLogIn/', views.ClientLogInView.as_view(), name='client_log_in'),

    path('getClientsGroup/', views.GetClientsGroupView.as_view(), name='get_clients_group'),
    path('addClientsGroup/', views.AddClientsGroupView.as_view(), name='add_clients_group'),
    path('removeClientsGroup/', views.RemoveClientsGroupView.as_view(), name='remove_clients_group'),

    path('getOrder/', views.GetOrderView.as_view(), name='get_order'),
    path('addOrder/', views.AddOrderView.as_view(), name='add_order'),
    path('removeOrder/', views.RemoveOrderView.as_view(), name='remove_order'),
    path('setPaymentTrue/', views.SetPaymentTrueView.as_view(), name='set_payment_true'),

    path('getTransaction/', views.GetTransactionView.as_view(), name='get_transaction'),

    path('getRate/', views.GetRateView.as_view(), name='get_rate'),
    path('addRate/', views.AddRateView.as_view(), name='add_rate'),
    path('removeRate/', views.RemoveRateView.as_view(), name='remove_rate'),
    path('changeRate/', views.ChangeRateDataView.as_view(), name='change_rate'),
    path('addRateToGroup/', views.AddRateToGroupView.as_view(), name='add_rate_to_group'),
    path('removeRateFromGroup/', views.RemoveRateFromGroupView.as_view(), name='remove_rate_from_group'),

    path('getRateGroup/', views.GetRateGroupView.as_view(), name='get_rate_group'),
    path('addRateGroup/', views.AddRateGroupView.as_view(), name='add_rate_group'),
    path('removeRateGroup/', views.RemoveRateGroupView.as_view(), name="remove_rate_group")

]
