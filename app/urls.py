# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('projinfo', views.home, name='playbookinfo'),
    path('day0', views.executePlaybook, name='playbookday0'),
    path('hello',views.hellow,name="firstpage")

    # # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
