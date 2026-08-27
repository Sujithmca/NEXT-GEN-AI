from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    path("login/", account_views.login, name="login"),
    path("admin-login/", account_views.admin_login, name="admin_login"),
    path("register/", account_views.register, name="register"),
    path("logout/", account_views.logout, name="logout"),
    path("profile/", account_views.profile, name="profile"),
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("team/", include("team.urls")),
    path("events/", include("events.urls")),
    path("projects/", include("projects.urls")),
    path("resources/", include("resources.urls")),
    path("learning/", include("learning.urls")),
    path("news/", include("news.urls")),
    path("gallery/", include("gallery.urls")),
    path("accounts/", include("accounts.urls")),
    path("management/", include("management.urls")),
    path("achievements/", include("achievements.urls")),
    path("community/", include("community.urls")),
    path("chatbot/", include("chatbot.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
