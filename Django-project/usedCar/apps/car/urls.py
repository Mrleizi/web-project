# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.car import views

urlpatterns = [
    url(r'^carlist/', views.carlist, name='carlist'),
    url(r'^release/', views.info_message, name='release'),
    url(r'^price0_10/', views.price0_10, name='price0_10'),
    url(r'^price10_30/', views.price10_30, name='price10_30'),
    url(r'^price30_80/', views.price30_80, name='price30_80'),
    url(r'^price80_/', views.price80_, name='price80_'),
    url(r'^detail/(?P<id>\d+)/', views.car_detail, name='detail'),
    url(r'^car_cancel/(?P<id>\d+)/', views.car_cancel, name='car_cancel'),
    url(r'^alterprice/(?P<id>\d+)/', views.alterprice, name='alterprice')

]
