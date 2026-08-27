from django.shortcuts import render
from django.http import JsonResponse

from core.json_storage import load_json


def resources_list(request):

    resources = load_json("resources.json")

    category = request.GET.get("category", "").strip()
    resource_type = request.GET.get(
        "type",
        ""
    ).strip()

    search = request.GET.get(
        "search",
        ""
    ).strip().lower()


    if category:

        resources = [
            resource for resource in resources
            if resource.get("category") == category
        ]


    if resource_type:

        resources = [
            resource for resource in resources
            if resource.get("resource_type") == resource_type
        ]


    if search:

        resources = [
            resource for resource in resources
            if search in resource.get(
                "title",
                ""
            ).lower()
            or search in resource.get(
                "description",
                ""
            ).lower()
            or search in resource.get(
                "category",
                ""
            ).lower()
        ]


    all_resources = load_json(
        "resources.json"
    )


    categories = sorted(
        set(
            resource.get("category")
            for resource in all_resources
            if resource.get("category")
        )
    )


    resource_types = sorted(
        set(
            resource.get("resource_type")
            for resource in all_resources
            if resource.get("resource_type")
        )
    )


    return render(
        request,
        "resources/resources.html",
        {
            "resources": resources,
            "categories": categories,
            "resource_types": resource_types,
            "selected_category": category,
            "selected_type": resource_type,
            "search_query": search
        }
    )


def resources_api(request):

    resources = load_json(
        "resources.json"
    )

    return JsonResponse(
        resources,
        safe=False
    )