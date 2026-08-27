from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [

    path(
        "",
        views.projects_list,
        name="projects"
    ),

    path(
        "api/",
        views.projects_api,
        name="projects_api"
    ),

    path(
        "<int:project_id>/",
        views.project_detail,
        name="detail"
    ),

    path(
        "achievements/",
        views.achievements,
        name="achievements"
    ),
]