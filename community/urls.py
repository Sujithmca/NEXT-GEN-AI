from django.urls import path

from . import views

app_name = "community"

urlpatterns = [
    path("", views.home, name="home"),
    path("join/", views.join_club, name="join"),
]
