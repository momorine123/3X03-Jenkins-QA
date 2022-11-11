from django.urls import path

from . import views

import mfa

urlpatterns = [
    #authentication
    path('', views.dashboardRedirect, name='dashboardRedirect'),
    path('auth/login',views.loginView, name = "login"),
    path('auth/logout', views.logoutView, name="logout"),
    path("wrong_user/",views.wrong_user,name='wrong_user'),
    path("accounts/profile/",views.mfa_redirect,name='mfa_redirect'),

    #IT paths
    path('it/home/', views.it_home, name='it-home'),
    path("it/accounts/",views.account_management, name = "account-management"),
    path("it/accounts/register/",views.register_request, name = "register-request"),
    path("it/accounts/update/<slug:slug>/",views.update_request, name = "update-request"),
    path("it/accounts/update/<slug:slug>/password",views.update_password, name = "update-password"),
    path('it/add_assets/', views.add_assets, name='add-assets'),
    path('it/update_assets/<slug:slug>/', views.update_assets, name='update-assets'),
    path('it/delete_assets/<slug:slug>/', views.delete_assets, name='delete-assets'),
    path('it/unlock_username/', views.unlock_username, name='unlock-username'),
    path('it/unlock_ip/', views.unlock_ip, name='unlock-ip'),

    #staff paths
    path('staff/home/', views.staff_home, name='staff-home'),
    path('staff/requested_list/',views.requested_list, name = 'requested-list'),
    path('staff/staff_request/<slug:slug>/',views.staff_request, name = 'staff-request'),

    #manager paths
    path('manager/home/', views.manager_home, name='manager-home'),
    path('manager/request_to/', views.request_to, name='request-to'),
    path('manager/manager_request_to/<slug:slug>', views.manager_update_request_to, name='request-to-by-manager'),
    path('manager/manager_reject_to/<slug:slug>', views.manager_delete_request_to, name='reject-to-by-manager'),

    path('manager/request_from/', views.request_from_list, name='request-from'),
    path('manager/manager_request_from/<slug:slug>', views.manager_request_from, name='request-from-manager'),
    path('manager/approve/<slug:slug>/', views.approve, name='approve'),

    path('manager/inventory_management', views.inventory_management, name='inventory-management'),
    path('manager/inventory_list', views.inventory_list, name='inventory-list'),
    path('manager/manage_inventory_list/<slug:slug>/', views.manager_update_assets, name='manage-inventory-list'),
    path('manager/manage_delete_assets/<slug:slug>/', views.manager_delete_assets, name='manage-delete-assets'),

    path('manager/select/<slug:slug>/', views.select, name='select'),
    path('manager/select_list', views.select_list, name='select-list'),

]