from django.urls import path

from . import views


app_name = "management"


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # TEAM
    path(
        "team/",
        views.team_list,
        name="team_list"
    ),

    path(
        "team/create/",
        views.team_create,
        name="team_create"
    ),

    path(
        "team/<int:item_id>/edit/",
        views.team_update,
        name="team_update"
    ),

    path(
        "team/<int:item_id>/delete/",
        views.team_delete,
        name="team_delete"
    ),

    # EVENTS
    path(
        "events/",
        views.events_list,
        name="events_list"
    ),

    path(
        "events/create/",
        views.event_create,
        name="event_create"
    ),

    path(
        "events/<int:item_id>/edit/",
        views.event_update,
        name="event_update"
    ),

    path(
        "events/<int:item_id>/delete/",
        views.event_delete,
        name="event_delete"
    ),

    # PROJECTS
    path(
        "projects/",
        views.projects_list,
        name="projects_list"
    ),

    path(
        "projects/create/",
        views.project_create,
        name="project_create"
    ),

    path(
        "projects/<int:item_id>/edit/",
        views.project_update,
        name="project_update"
    ),

    path(
        "projects/<int:item_id>/delete/",
        views.project_delete,
        name="project_delete"
    ),

    # ACHIEVEMENTS
    path(
        "achievements/",
        views.achievements_list,
        name="achievements_list"
    ),

    path(
        "achievements/create/",
        views.achievement_create,
        name="achievement_create"
    ),

    path(
        "achievements/<int:item_id>/edit/",
        views.achievement_update,
        name="achievement_update"
    ),

    path(
        "achievements/<int:item_id>/delete/",
        views.achievement_delete,
        name="achievement_delete"
    ),

    # RESOURCES
    path(
        "resources/",
        views.resources_list,
        name="resources_list"
    ),

    path(
        "resources/create/",
        views.resource_create,
        name="resource_create"
    ),

    path(
        "resources/<int:item_id>/edit/",
        views.resource_update,
        name="resource_update"
    ),

    path(
        "resources/<int:item_id>/delete/",
        views.resource_delete,
        name="resource_delete"
    ),

    # NEWS
    path(
        "news/",
        views.news_list,
        name="news_list"
    ),

    path(
        "news/create/",
        views.news_create,
        name="news_create"
    ),

    path(
        "news/<int:item_id>/edit/",
        views.news_update,
        name="news_update"
    ),

    path(
        "news/<int:item_id>/delete/",
        views.news_delete,
        name="news_delete"
    ),

    # GALLERY
    path(
        "gallery/",
        views.gallery_list,
        name="gallery_list"
    ),

    path(
        "gallery/create/",
        views.gallery_create,
        name="gallery_create"
    ),

    path(
        "gallery/<int:item_id>/edit/",
        views.gallery_update,
        name="gallery_update"
    ),

    path(
        "gallery/<int:item_id>/delete/",
        views.gallery_delete,
        name="gallery_delete"
    ),

    # REGISTRATIONS
    path(
        "registrations/",
        views.registrations,
        name="registrations"
    ),

    path(
        "members/<int:member_id>/",
        views.member_detail,
        name="member_detail"
    ),

    # API
    path(
        "api/stats/",
        views.dashboard_stats_api,
        name="dashboard_stats"
    ),
]