# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.order import views

urlpatterns = [
    url(r'^create_order/(?P<id>\d+)/', views.create_order, name='create_order'),
    url(r'^order/(?P<id>\d+)/', views.order, name='order'),
    url(r'^cancel_order/(?P<id>\d+)/', views.cancel_order, name='cancel_order'),
    url(r'^ensure_order/(?P<id>\d+)/', views.ensure_order, name='ensure_order')

]
