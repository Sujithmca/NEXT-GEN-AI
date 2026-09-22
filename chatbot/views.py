from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import ask_ai


@require_POST
def chat(request):

    message = request.POST.get(
        "message",
        ""
    ).strip()

    if not message:
        return JsonResponse(
            {
                "success": False,
                "error": "Please enter a message."
            },
            status=400
        )

    # Send message to AI
    ai_response = ask_ai(message)

    return JsonResponse(
        {
            "success": True,
            "message": ai_response
        }
    )