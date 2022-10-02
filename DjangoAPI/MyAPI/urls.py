
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('form/', views.myform, name='myform'),
    path('api/', include(routers.urls)),
    path('status/', views.approvereject),
]
