# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path,include
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('projinfo', views.home, name='playbookinfo'),
    path('day0', views.executePlaybook, name='playbookday0'),
    path('hello',views.hellow,name="firstpage"),
    path('api-auth/', include('rest_framework.urls')),
    #path('todos/', include(todo_urls)),
    path('api', views.TodoListApiView.as_view()),
    path('api/<int:id>/', views.TodoDetailApiView.as_view()),

    # # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
