from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views

from api.views import *

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
]
