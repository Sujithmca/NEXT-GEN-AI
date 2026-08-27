import json
from pathlib import Path

from django.conf import settings


DATA_FILES = {
    "team": "team.json",
    "events": "events.json",
    "projects": "projects.json",
    "achievements": "achievements.json",
    "resources": "resources.json",
    "news": "news.json",
    "gallery": "gallery.json",
}


def load_data(filename):

    file_path = settings.BASE_DIR / "data" / filename

    try:

        if not file_path.exists():
            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):

        return []


def get_club_context():

    context = {}

    for name, filename in DATA_FILES.items():

        context[name] = load_data(filename)

    return context