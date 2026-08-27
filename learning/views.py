from django.shortcuts import render
from django.http import JsonResponse

from core.json_storage import load_json


def learning_hub(request):

    learning_data = load_json("learning.json")

    category = request.GET.get(
        "category",
        ""
    ).strip()

    level = request.GET.get(
        "level",
        ""
    ).strip()

    search = request.GET.get(
        "search",
        ""
    ).strip().lower()


    if category:

        learning_data = [
            item for item in learning_data
            if item.get("title") == category
        ]


    if level:

        learning_data = [
            item for item in learning_data
            if item.get("level") == level
        ]


    if search:

        learning_data = [
            item for item in learning_data
            if search in item.get(
                "title",
                ""
            ).lower()
            or search in item.get(
                "description",
                ""
            ).lower()
            or any(
                search in topic.lower()
                for topic in item.get(
                    "topics",
                    []
                )
            )
        ]


    all_data = load_json("learning.json")


    categories = sorted(
        set(
            item.get("title")
            for item in all_data
            if item.get("title")
        )
    )


    levels = sorted(
        set(
            item.get("level")
            for item in all_data
            if item.get("level")
        )
    )


    return render(
        request,
        "learning/learning.html",
        {
            "learning": learning_data,
            "categories": categories,
            "levels": levels,
            "selected_category": category,
            "selected_level": level,
            "search_query": search
        }
    )


def learning_detail(request, learning_id):

    learning_data = load_json(
        "learning.json"
    )

    item = next(
        (
            item for item in learning_data
            if item.get("id") == learning_id
        ),
        None
    )


    if not item:

        return render(
            request,
            "404.html",
            status=404
        )


    return render(
        request,
        "learning/detail.html",
        {
            "learning": item
        }
    )


def learning_api(request):

    data = load_json(
        "learning.json"
    )

    return JsonResponse(
        data,
        safe=False
    )