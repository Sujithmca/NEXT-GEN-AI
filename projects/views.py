from django.shortcuts import render
from django.http import JsonResponse
from core.json_storage import load_json


def projects_list(request):

    projects = load_json("projects.json")

    category = request.GET.get("category", "").strip()
    search = request.GET.get("search", "").strip().lower()

    if category:
        projects = [
            project for project in projects
            if project.get("category") == category
        ]

    if search:
        projects = [
            project for project in projects
            if search in project.get("title", "").lower()
            or search in project.get("description", "").lower()
            or search in project.get("category", "").lower()
            or any(
                search in tech.lower()
                for tech in project.get("technologies", [])
            )
        ]

    categories = sorted(
        set(
            project.get("category")
            for project in load_json("projects.json")
            if project.get("category")
        )
    )

    featured_projects = [
        project for project in projects
        if project.get("is_featured", False)
    ]

    return render(
        request,
        "projects/projects.html",
        {
            "projects": projects,
            "featured_projects": featured_projects,
            "categories": categories,
            "selected_category": category,
            "search_query": search,
        }
    )


def project_detail(request, project_id):

    projects = load_json("projects.json")

    project = next(
        (
            project for project in projects
            if project.get("id") == project_id
        ),
        None
    )

    if not project:
        return render(
            request,
            "404.html",
            status=404
        )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project
        }
    )


def projects_api(request):

    projects = load_json("projects.json")

    return JsonResponse(
        projects,
        safe=False
    )


def achievements(request):

    data = load_json("achievements.json")

    return render(
        request,
        "projects/achievements.html",
        {
            "achievements": data
        }
    )