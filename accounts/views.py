from django.contrib.auth import logout as django_logout
from django.core.cache import cache
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .decorators import login_required_custom
from .utils import (
	MemberExistsError,
	authenticate_member,
	create_member,
	find_user_by_email,
	find_user_by_username,
	load_members,
	public_member,
	strong_password,
	valid_phone,
	valid_username,
)


DEPARTMENTS = ["MCA", "M.Sc Computer Science", "BCA", "B.Sc Computer Science", "Other"]
YEARS = ["I Year", "II Year", "III Year", "IV Year"]
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300


def _json_request(request):
	return request.headers.get("X-Requested-With") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", "")


def _response(request, payload, status=200, redirect_to=None, template_name="accounts/register.html"):
	if _json_request(request):
		return JsonResponse(payload, status=status)
	if redirect_to:
		return redirect(redirect_to)
	return render(request, template_name, {"errors": payload.get("errors", {}), "values": request.POST, "admin_mode": getattr(request, "admin_mode", False)})


@require_http_methods(["GET", "POST"])
def register(request):
	if request.session.get("member_id"):
		return redirect("/")
	if request.method == "GET":
		return render(request, "accounts/register.html", {"departments": DEPARTMENTS, "years": YEARS})

	values = {key: request.POST.get(key, "").strip() for key in ("full_name", "username", "email", "phone", "department", "year")}
	password = request.POST.get("password", "")
	confirm_password = request.POST.get("confirm_password", "")
	errors = {}

	if not values["full_name"] or len(values["full_name"]) > 100:
		errors["full_name"] = "Enter your full name."
	if not valid_username(values["username"]):
		errors["username"] = "Use 3-30 letters, numbers, dots, dashes, or underscores."
	elif find_user_by_username(values["username"]):
		errors["username"] = "That username is already registered."
	try:
		validate_email(values["email"])
	except Exception:
		errors["email"] = "Enter a valid email address."
	if values["email"] and find_user_by_email(values["email"]):
		errors["email"] = "That email is already registered."
	if not valid_phone(values["phone"]):
		errors["phone"] = "Enter 10-15 digits only."
	if values["department"] not in DEPARTMENTS:
		errors["department"] = "Choose a valid department."
	if values["year"] not in YEARS:
		errors["year"] = "Choose a valid year of study."
	if not strong_password(password):
		errors["password"] = "Use 8+ characters with uppercase, lowercase, number, and special character."
	if password != confirm_password:
		errors["confirm_password"] = "Passwords do not match."

	if errors:
		return _response(request, {"success": False, "errors": errors}, status=400)

	try:
		create_member({**values, "password": password})
	except MemberExistsError:
		return _response(request, {"success": False, "errors": {"username": "Username or email is already registered."}}, status=409)
	return _response(request, {"success": True, "message": "Registration complete. Please log in."}, redirect_to=reverse("accounts:login"))


@require_http_methods(["GET", "POST"])
def login(request):
	return _login(request, admin_only=False)


@require_http_methods(["GET", "POST"])
def admin_login(request):
	return _login(request, admin_only=True)


def _login(request, admin_only=False):
	request.admin_mode = admin_only
	if request.session.get("member_id"):
		return redirect("/")
	default_next = reverse("management:dashboard") if admin_only else "/"
	next_url = request.GET.get("next", default_next) if request.method == "GET" else request.POST.get("next", default_next)
	if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
		next_url = default_next
	if request.method == "GET":
		return render(request, "accounts/login.html", {"next": next_url, "admin_mode": admin_only})

	identifier = request.POST.get("identifier", "").strip()
	password = request.POST.get("password", "")
	rate_key = f"login-attempts:{request.META.get('REMOTE_ADDR', 'unknown')}"
	attempts = cache.get(rate_key, 0)
	if attempts >= MAX_LOGIN_ATTEMPTS:
		payload = {"success": False, "error": "Too many login attempts. Please try again in a few minutes."}
		return _response(request, payload, status=429, template_name="accounts/login.html")

	member = authenticate_member(identifier, password)
	if not member or (admin_only and member.get("role") != "admin"):
		cache.set(rate_key, attempts + 1, LOGIN_WINDOW_SECONDS)
		return _response(request, {"success": False, "error": "Invalid username/email or password."}, status=401, template_name="accounts/login.html")

	cache.delete(rate_key)
	request.session.flush()
	request.session["member_id"] = member["id"]
	request.session["username"] = member["username"]
	request.session["role"] = member.get("role", "member")
	request.session["is_authenticated"] = True
	request.session["joined_club"] = bool(member.get("club_member", False))
	if request.POST.get("remember_me") != "on":
		request.session.set_expiry(0)
	return _response(request, {"success": True, "redirect": next_url}, redirect_to=next_url)


@require_http_methods(["POST"])
def logout(request):
	request.session.flush()
	django_logout(request)
	if _json_request(request):
		return JsonResponse({"success": True, "redirect": reverse("accounts:login")})
	return redirect("accounts:login")


@login_required_custom
def profile(request):
	member = next((item for item in load_members() if item.get("id") == request.session.get("member_id")), None)
	if not member:
		request.session.flush()
		return redirect("accounts:login")
	return render(request, "accounts/profile.html", {"member": public_member(member)})
