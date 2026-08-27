from functools import wraps

from django.http import JsonResponse
from django.shortcuts import redirect, render


def _wants_json(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", "")


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("member_id"):
            if _wants_json(request):
                return JsonResponse({"success": False, "error": "Your session has expired. Please log in again."}, status=401)
            return redirect(f"/accounts/login/?next={request.path}")
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required_custom(view_func):
    @wraps(view_func)
    @login_required_custom
    def wrapper(request, *args, **kwargs):
        if request.session.get("role") != "admin":
            return render(request, "management/access_denied.html", status=403)
        return view_func(request, *args, **kwargs)

    return wrapper
