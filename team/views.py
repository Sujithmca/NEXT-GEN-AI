from django.shortcuts import render
from core.json_storage import load_json


def team_list(request):
    team_members = load_json("team.json")

    active_members = [
        member for member in team_members
        if member.get("is_active", True)
    ]

    return render(
        request,
        "team.html",
        {
            "team_members": active_members
        }
    )