from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        views.login,
        name="login",
    ),
    path("admin-login/", views.admin_login, name="admin_login"),
    path(
        "logout/",
        views.logout,
        name="logout",
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
