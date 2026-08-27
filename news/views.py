from django.shortcuts import render
from django.http import JsonResponse

from core.json_storage import load_json


def news_list(request):

    news_data = load_json(
        "news.json"
    )

    category = request.GET.get(
        "category",
        ""
    ).strip()

    search = request.GET.get(
        "search",
        ""
    ).strip().lower()


    if category:

        news_data = [
            item for item in news_data
            if item.get("category") == category
        ]


    if search:

        news_data = [
            item for item in news_data
            if search in item.get(
                "title",
                ""
            ).lower()
            or search in item.get(
                "description",
                ""
            ).lower()
        ]


    all_news = load_json(
        "news.json"
    )


    categories = sorted(
        set(
            item.get("category")
            for item in all_news
            if item.get("category")
        )
    )


    featured = [
        item for item in news_data
        if item.get(
            "is_featured",
            False
        )
    ]


    return render(
        request,
        "news/news.html",
        {
            "news": news_data,
            "featured": featured,
            "categories": categories,
            "selected_category": category,
            "search_query": search
        }
    )


def news_detail(request, news_id):

    news_data = load_json(
        "news.json"
    )

    item = next(
        (
            item for item in news_data
            if item.get("id") == news_id
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
        "news/detail.html",
        {
            "news": item
        }
    )


def news_api(request):

    data = load_json(
        "news.json"
    )

    return JsonResponse(
        data,
        safe=False
    )