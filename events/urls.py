from django.urls import path
from . import views

app_name = "events"

urlpatterns = [

    path(
        "",
        views.events_list,
        name="events"
    ),

    path(
        "api/",
        views.events_api,
        name="events_api"
    ),

    path(
        "<int:event_id>/",
        views.event_detail,
        name="detail"
    ),

    path(
        "<int:event_id>/register/",
        views.register_event,
        name="register"
    ),
]