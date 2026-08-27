from django.shortcuts import render
from django.http import JsonResponse

from core.json_storage import load_json


def gallery_list(request):

    gallery_data = load_json(
        "gallery.json"
    )

    category = request.GET.get(
        "category",
        ""
    ).strip()


    if category:

        gallery_data = [
            item for item in gallery_data
            if item.get("category") == category
        ]


    all_gallery = load_json(
        "gallery.json"
    )


    categories = sorted(
        set(
            item.get("category")
            for item in all_gallery
            if item.get("category")
        )
    )


    return render(
        request,
        "gallery/gallery.html",
        {
            "gallery": gallery_data,
            "categories": categories,
            "selected_category": category
        }
    )


def gallery_api(request):

    data = load_json(
        "gallery.json"
    )

    return JsonResponse(
        data,
        safe=False
    )