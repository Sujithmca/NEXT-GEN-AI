from django.urls import path

from . import views


app_name = "news"


urlpatterns = [

    path(
        "",
        views.news_list,
        name="news"
    ),

    path(
        "api/",
        views.news_api,
        name="api"
    ),

    path(
        "<int:news_id>/",
        views.news_detail,
        name="detail"
    ),

]