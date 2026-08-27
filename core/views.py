from django.http import JsonResponse
from django.shortcuts import render

from .json_storage import load_json


def home(request):

    # Load JSON data
    team = load_json("team.json")
    projects = load_json("projects.json")
    events = load_json("events.json")
    achievements = load_json("achievements.json")

    # Count only active team members
    active_members = [
        member
        for member in team
        if member.get("is_active", True)
    ]

    # Dynamic statistics
    statistics = {
        "members": len(active_members),
        "projects": len(projects),
        "events": len(events),
        "achievements": len(achievements),
    }

    # Featured projects
    featured_projects = [
        project
        for project in projects
        if project.get("is_featured", False)
    ]

    context = {
        "statistics": statistics,
        "featured_projects": featured_projects[:3],
    }

    return render(
        request,
        "home.html",
        context
    )


def search(request):
    query = request.GET.get("q", "").strip()[:80]
    if not query:
        return JsonResponse({"results": []})

    query_terms = query.casefold().split()
    searchable_files = {
        "Events": "events.json",
        "Projects": "projects.json",
        "Team": "team.json",
        "Resources": "resources.json",
        "Learning": "learning.json",
        "News": "news.json",
    }
    results = []
    for category, filename in searchable_files.items():
        for item in load_json(filename):
            public_text = " ".join(
                str(value) for key, value in item.items()
                if key not in {"password", "email", "phone"}
            ).casefold()
            if all(term in public_text for term in query_terms):
                title = item.get("title") or item.get("name") or item.get("full_name") or category
                results.append({
                    "category": category,
                    "title": str(title)[:120],
                    "description": str(item.get("description", item.get("role", "")))[:180],
                })
    return JsonResponse({"results": results[:20]})