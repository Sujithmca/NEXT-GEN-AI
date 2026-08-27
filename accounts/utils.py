import json
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password


MEMBERS_FILE = Path(settings.BASE_DIR) / "data" / "members.json"
_STORAGE_LOCK = threading.RLock()
_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
_PHONE_PATTERN = re.compile(r"^\d{10,15}$")


class MemberExistsError(Exception):
    pass


def _ensure_members_file():
    MEMBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not MEMBERS_FILE.exists():
        MEMBERS_FILE.write_text(json.dumps({"members": []}, indent=2), encoding="utf-8")


def load_members():
    """Load members safely; malformed storage is treated as unavailable."""
    with _STORAGE_LOCK:
        _ensure_members_file()
        try:
            data = json.loads(MEMBERS_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    members = data.get("members", []) if isinstance(data, dict) else []
    return members if isinstance(members, list) else []


def save_members(members):
    """Atomically replace the member file to avoid partial JSON writes."""
    with _STORAGE_LOCK:
        _ensure_members_file()
        temporary_file = MEMBERS_FILE.with_suffix(".tmp")
        temporary_file.write_text(
            json.dumps({"members": members}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary_file.replace(MEMBERS_FILE)


def find_user_by_username(username):
    normalized = username.strip().casefold()
    return next(
        (member for member in load_members() if str(member.get("username", "")).casefold() == normalized),
        None,
    )


def find_user_by_email(email):
    normalized = email.strip().casefold()
    return next(
        (member for member in load_members() if str(member.get("email", "")).casefold() == normalized),
        None,
    )


def create_member(member_data):
    with _STORAGE_LOCK:
        members = load_members()
        if any(
            str(item.get("username", "")).casefold() == member_data["username"].casefold()
            for item in members
        ) or any(
            str(item.get("email", "")).casefold() == member_data["email"].casefold()
            for item in members
        ):
            raise MemberExistsError
        member = {
            "id": max((int(item.get("id", 0)) for item in members if str(item.get("id", "")).isdigit()), default=0) + 1,
            "full_name": member_data["full_name"],
            "username": member_data["username"],
            "email": member_data["email"],
            "phone": member_data["phone"],
            "password": make_password(member_data["password"]),
            "department": member_data["department"],
            "year": member_data["year"],
            "role": "member",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        members.append(member)
        save_members(members)
    return member


def authenticate_member(identifier, password):
    member = find_user_by_email(identifier) or find_user_by_username(identifier)
    if not member or not check_password(password, member.get("password", "")):
        return None
    return member


def update_member(member_id, updates):
    with _STORAGE_LOCK:
        members = load_members()
        for member in members:
            if str(member.get("id")) == str(member_id):
                member.update(updates)
                save_members(members)
                return member
    return None


def public_member(member):
    return {key: value for key, value in member.items() if key != "password"}


def valid_username(username):
    return bool(_USERNAME_PATTERN.fullmatch(username))


def valid_phone(phone):
    return bool(_PHONE_PATTERN.fullmatch(phone))


def strong_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )
