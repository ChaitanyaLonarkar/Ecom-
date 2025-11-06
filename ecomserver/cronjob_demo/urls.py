
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .cron import *

urlpatterns = [
    path('', CronJobDemo.as_view(),name="cron_job"  )]