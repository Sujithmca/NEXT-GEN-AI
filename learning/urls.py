from django.urls import path

from . import views


app_name = "learning"


urlpatterns = [

    path(
        "",
        views.learning_hub,
        name="learning"
    ),

    path(
        "api/",
        views.learning_api,
        name="api"
    ),

    path(
        "<int:learning_id>/",
        views.learning_detail,
        name="detail"
    ),

]