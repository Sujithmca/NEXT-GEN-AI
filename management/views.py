import os
import uuid
import json

from django.conf import settings
from pathlib import Path
from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from accounts.decorators import admin_required_custom
from accounts.utils import load_members, public_member


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# =========================================================
# ADMIN ONLY DECORATOR
# =========================================================

admin_required = admin_required_custom


# =========================================================
# JSON STORAGE
# =========================================================

def load_json(filename):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = DATA_DIR / filename

    if not file_path.exists():

        file_path.write_text(
            "[]",
            encoding="utf-8"
        )

        return []

    try:

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            return []

        data = json.loads(content)

        return data if isinstance(data, list) else []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_json(filename, data):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = DATA_DIR / filename

    temp_file = file_path.with_suffix(".tmp")

    temp_file.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    temp_file.replace(file_path)


def get_next_id(data):

    ids = []

    for item in data:

        try:
            ids.append(
                int(item.get("id", 0))
            )

        except (
            TypeError,
            ValueError
        ):
            continue

    return max(ids, default=0) + 1


def get_item_by_id(data, item_id):
    for item in data:
        if str(item.get("id")) == str(item_id):
            return item

    return None


def get_list_url_name(data_file):
    url_names = {
        "team.json": "management:team_list",
        "events.json": "management:events_list",
        "projects.json": "management:projects_list",
        "achievements.json": "management:achievements_list",
        "resources.json": "management:resources_list",
        "news.json": "management:news_list",
        "gallery.json": "management:gallery_list",
    }

    return url_names.get(data_file)

def save_team_photo(request):

    photo = request.FILES.get("profile_image")

    if not photo:
        return None

    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    extension = os.path.splitext(
        photo.name
    )[1].lower()

    if extension not in allowed_extensions:
        return None

    # Maximum 2 MB
    if photo.size > 2 * 1024 * 1024:
        return None

    team_folder = (
        settings.MEDIA_ROOT / "team"
    )

    team_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = (
        team_folder / filename
    )

    with open(
        file_path,
        "wb+"
    ) as destination:

        for chunk in photo.chunks():
            destination.write(chunk)

    return f"team/{filename}"


# =========================================================
# DASHBOARD
# =========================================================

@admin_required
def dashboard(request):

    joined_members = [
        public_member(member)
        for member in load_members()
        if member.get("club_member", False)
    ]

    context = {
        "team_count": len(load_json("team.json")),
        "event_count": len(load_json("events.json")),
        "project_count": len(load_json("projects.json")),
        "achievement_count": len(
            load_json("achievements.json")
        ),
        "resource_count": len(
            load_json("resources.json")
        ),
        "news_count": len(load_json("news.json")),
        "gallery_count": len(
            load_json("gallery.json")
        ),
        "registration_count": len(
            load_json("registrations.json")
        ),
        "joined_members": joined_members,
    }

    return render(
        request,
        "management/dashboard.html",
        context
    )


# =========================================================
# GENERIC LIST
# =========================================================

@admin_required
def item_list(request, data_file, title):

    items = load_json(data_file)

    return render(
        request,
        "management/item_list.html",
        {
            "items": items,
            "title": title,
            "data_file": data_file,
        }
    )


# =========================================================
# GENERIC CREATE
# =========================================================

@admin_required
def item_create(
    request,
    data_file,
    title,
    fields
):

    if request.method == "POST":

        data = load_json(data_file)

        new_item = {
            "id": get_next_id(data)
        }

        for field in fields:

            new_item[field] = request.POST.get(
                field,
                ""
            ).strip()

        data.append(new_item)

        save_json(
            data_file,
            data
        )

        messages.success(
            request,
            f"{title} created successfully!"
        )

        return redirect(
           get_item_list_url(data_file)
        )

    return render(
        request,
        "management/item_form.html",
        {
            "title": f"Add {title}",
            "fields": fields,
            "item": {},
            "data_file": data_file,
        }
    )


# =========================================================
# GENERIC UPDATE
# =========================================================

@admin_required
def item_update(
    request,
    data_file,
    title,
    fields,
    item_id
):

    data = load_json(data_file)

    item = get_item_by_id(
        data,
        item_id
    )

    if item is None:

        messages.error(
            request,
            f"{title} not found."
        )

        return redirect(
            get_list_url_name(data_file)
        )

    if request.method == "POST":

        for field in fields:

            item[field] = request.POST.get(
                field,
                ""
            ).strip()

        save_json(
            data_file,
            data
        )

        messages.success(
            request,
            f"{title} updated successfully!"
        )

        return redirect(
            "management:item_list",
            data_file=data_file,
            title=title
        )

    return render(
        request,
        "management/item_form.html",
        {
            "title": f"Edit {title}",
            "fields": fields,
            "item": item,
            "data_file": data_file,
        }
    )


# =========================================================
# GENERIC DELETE
# =========================================================

@admin_required
@require_POST
def item_delete(
    request,
    data_file,
    title,
    item_id
):

    data = load_json(data_file)

    new_data = [
        item
        for item in data
        if str(item.get("id")) != str(item_id)
    ]

    if len(new_data) == len(data):

        messages.error(
            request,
            f"{title} not found."
        )

    else:

        save_json(
            data_file,
            new_data
        )

        messages.success(
            request,
            f"{title} deleted successfully!"
        )

    return redirect(
        get_item_list_url(data_file)
    )


# =========================================================
# TEAM
# =========================================================

TEAM_FIELDS = [
    "name",
    "role",
    "department",
    "bio",
    "profile_image",
    "linkedin",
    "github",
    "is_active",
]


@admin_required
def team_list(request):
    return item_list(
        request,
        "team.json",
        "Team"
    )


@admin_required
def team_create(request):

    if request.method == "POST":

        data = load_json("team.json")

        new_item = {
            "id": get_next_id(data),
            "name": request.POST.get(
                "name",
                ""
            ).strip(),

            "role": request.POST.get(
                "role",
                ""
            ).strip(),

            "department": request.POST.get(
                "department",
                ""
            ).strip(),

            "bio": request.POST.get(
                "bio",
                ""
            ).strip(),

            "profile_image": "",

            "linkedin": request.POST.get(
                "linkedin",
                ""
            ).strip(),

            "github": request.POST.get(
                "github",
                ""
            ).strip(),

            "is_active": request.POST.get(
                "is_active",
                ""
            ).strip(),
        }

        photo_path = save_team_photo(request)

        if photo_path:
            new_item["profile_image"] = photo_path

        data.append(new_item)

        save_json(
            "team.json",
            data
        )

        messages.success(
            request,
            "Team member created successfully!"
        )

        return redirect(
            "management:team_list"
        )

    return render(
        request,
        "management/team_form.html",
        {
            "title": "Add Team Member",
            "item": {},
        }
    )


@admin_required
def team_update(request, item_id):

    data = load_json("team.json")

    item = get_item_by_id(
        data,
        item_id
    )

    if item is None:

        messages.error(
            request,
            "Team member not found."
        )

        return redirect(
            "management:team_list"
        )

    if request.method == "POST":

        item["name"] = request.POST.get(
            "name",
            ""
        ).strip()

        item["role"] = request.POST.get(
            "role",
            ""
        ).strip()

        item["department"] = request.POST.get(
            "department",
            ""
        ).strip()

        item["bio"] = request.POST.get(
            "bio",
            ""
        ).strip()

        item["linkedin"] = request.POST.get(
            "linkedin",
            ""
        ).strip()

        item["github"] = request.POST.get(
            "github",
            ""
        ).strip()

        item["is_active"] = request.POST.get(
            "is_active",
            ""
        ).strip()

        photo_path = save_team_photo(request)

        if photo_path:
            item["profile_image"] = photo_path

        save_json(
            "team.json",
            data
        )

        messages.success(
            request,
            "Team member updated successfully!"
        )

        return redirect(
            "management:team_list"
        )

    return render(
        request,
        "management/team_form.html",
        {
            "title": "Edit Team Member",
            "item": item,
        }
    )

@admin_required
@require_POST
def team_delete(request, item_id):
    return item_delete(
        request,
        "team.json",
        "Team Member",
        item_id
    )


# =========================================================
# EVENTS
# =========================================================

EVENT_FIELDS = [
    "title",
    "description",
    "category",
    "date",
    "start_time",
    "end_time",
    "venue",
    "banner_image",
    "registration_link",
    "is_upcoming",
]


@admin_required
def events_list(request):
    return item_list(
        request,
        "events.json",
        "Events"
    )


@admin_required
def event_create(request):
    return item_create(
        request,
        "events.json",
        "Event",
        EVENT_FIELDS
    )


@admin_required
def event_update(request, item_id):
    return item_update(
        request,
        "events.json",
        "Event",
        EVENT_FIELDS,
        item_id
    )


@admin_required
@require_POST
def event_delete(request, item_id):
    return item_delete(
        request,
        "events.json",
        "Event",
        item_id
    )


# =========================================================
# PROJECTS
# =========================================================

PROJECT_FIELDS = [
    "title",
    "description",
    "category",
    "technologies",
    "student_name",
    "team_name",
    "image",
    "github_url",
    "demo_url",
    "is_featured",
]


@admin_required
def projects_list(request):
    return item_list(
        request,
        "projects.json",
        "Projects"
    )


@admin_required
def project_create(request):
    return item_create(
        request,
        "projects.json",
        "Project",
        PROJECT_FIELDS
    )


@admin_required
def project_update(request, item_id):
    return item_update(
        request,
        "projects.json",
        "Project",
        PROJECT_FIELDS,
        item_id
    )


@admin_required
@require_POST
def project_delete(request, item_id):
    return item_delete(
        request,
        "projects.json",
        "Project",
        item_id
    )


# =========================================================
# ACHIEVEMENTS
# =========================================================

ACHIEVEMENT_FIELDS = [
    "title",
    "description",
    "category",
    "student_name",
    "date",
    "image",
    "certificate_url",
]


@admin_required
def achievements_list(request):
    return item_list(
        request,
        "achievements.json",
        "Achievements"
    )


@admin_required
def achievement_create(request):
    return item_create(
        request,
        "achievements.json",
        "Achievement",
        ACHIEVEMENT_FIELDS
    )


@admin_required
def achievement_update(request, item_id):
    return item_update(
        request,
        "achievements.json",
        "Achievement",
        ACHIEVEMENT_FIELDS,
        item_id
    )


@admin_required
@require_POST
def achievement_delete(request, item_id):
    return item_delete(
        request,
        "achievements.json",
        "Achievement",
        item_id
    )


# =========================================================
# RESOURCES
# =========================================================

RESOURCE_FIELDS = [
    "title",
    "description",
    "category",
    "resource_type",
    "url",
    "thumbnail",
]


@admin_required
def resources_list(request):
    return item_list(
        request,
        "resources.json",
        "Resources"
    )


@admin_required
def resource_create(request):
    return item_create(
        request,
        "resources.json",
        "Resource",
        RESOURCE_FIELDS
    )


@admin_required
def resource_update(request, item_id):
    return item_update(
        request,
        "resources.json",
        "Resource",
        RESOURCE_FIELDS,
        item_id
    )


@admin_required
@require_POST
def resource_delete(request, item_id):
    return item_delete(
        request,
        "resources.json",
        "Resource",
        item_id
    )


# =========================================================
# NEWS
# =========================================================

NEWS_FIELDS = [
    "title",
    "description",
    "category",
    "date",
    "image",
]


@admin_required
def news_list(request):
    return item_list(
        request,
        "news.json",
        "News"
    )


@admin_required
def news_create(request):
    return item_create(
        request,
        "news.json",
        "News",
        NEWS_FIELDS
    )


@admin_required
def news_update(request, item_id):
    return item_update(
        request,
        "news.json",
        "News",
        NEWS_FIELDS,
        item_id
    )


@admin_required
@require_POST
def news_delete(request, item_id):
    return item_delete(
        request,
        "news.json",
        "News",
        item_id
    )


# =========================================================
# GALLERY
# =========================================================

GALLERY_FIELDS = [
    "title",
    "description",
    "category",
    "image",
    "date",
]


@admin_required
def gallery_list(request):
    return item_list(
        request,
        "gallery.json",
        "Gallery"
    )


@admin_required
def gallery_create(request):
    return item_create(
        request,
        "gallery.json",
        "Gallery",
        GALLERY_FIELDS
    )


@admin_required
def gallery_update(request, item_id):
    return item_update(
        request,
        "gallery.json",
        "Gallery",
        GALLERY_FIELDS,
        item_id
    )


@admin_required
@require_POST
def gallery_delete(request, item_id):
    return item_delete(
        request,
        "gallery.json",
        "Gallery",
        item_id
    )


# =========================================================
# REGISTRATIONS
# =========================================================

@admin_required
def registrations(request):

    data = load_json(
        "registrations.json"
    )


@admin_required
def member_detail(request, member_id):

    member = next(
        (
            item for item in load_members()
            if str(item.get("id")) == str(member_id)
            and item.get("club_member", False)
        ),
        None,
    )

    if not member:
        return render(request, "management/access_denied.html", status=404)

    return render(
        request,
        "management/member_detail.html",
        {"member": public_member(member)},
    )

    return render(
        request,
        "management/registrations.html",
        {
            "registrations": data
        }
    )


# =========================================================
# DASHBOARD API
# =========================================================

@admin_required
def dashboard_stats_api(request):

    return JsonResponse({

        "team": len(
            load_json("team.json")
        ),

        "events": len(
            load_json("events.json")
        ),

        "projects": len(
            load_json("projects.json")
        ),

        "achievements": len(
            load_json("achievements.json")
        ),

        "resources": len(
            load_json("resources.json")
        ),

        "news": len(
            load_json("news.json")
        ),

        "gallery": len(
            load_json("gallery.json")
        ),

        "registrations": len(
            load_json("registrations.json")
        ),
    })