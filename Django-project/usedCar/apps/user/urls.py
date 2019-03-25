# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.user import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^login_status', views.login_status, name='login_status'),

    url(r'^service/', views.service, name='service'),
    url(r'^protection/', views.protection, name='protection'),

    url(r'^user_info/', views.user_info, name='user_info'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^buyregister/', views.buyregister, name='buyregister')
]
