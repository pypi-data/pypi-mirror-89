"""Radicale urls."""

from django.urls import path

from . import views

app_name = 'kalabash_radicale'

urlpatterns = [
    path('', views.CalendarDetailView.as_view(),
         name="calendar_detail_view"),
]
