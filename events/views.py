from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

from core.json_storage import (
    load_json,
    save_json,
    create_item
)


def events_list(request):

    events = load_json("events.json")

    today = datetime.now().date()

    upcoming_events = []
    past_events = []

    for event in events:

        try:
            event_date = datetime.strptime(
                event["date"],
                "%Y-%m-%d"
            ).date()

            if event_date >= today:
                upcoming_events.append(event)
            else:
                past_events.append(event)

        except (ValueError, KeyError):
            continue

    upcoming_events.sort(key=lambda x: x["date"])
    past_events.sort(key=lambda x: x["date"], reverse=True)

    return render(
        request,
        "events/events.html",
        {
            "upcoming_events": upcoming_events,
            "past_events": past_events,
        }
    )


def event_detail(request, event_id):

    events = load_json("events.json")

    event = next(
        (event for event in events
         if event.get("id") == event_id),
        None
    )

    if not event:
        return render(
            request,
            "404.html",
            status=404
        )

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event
        }
    )


def register_event(request, event_id):

    events = load_json("events.json")

    event = next(
        (
            event for event in events
            if event.get("id") == event_id
        ),
        None
    )

    if not event:
        return render(
            request,
            "404.html",
            status=404
        )

    if request.method == "POST":

        name = request.POST.get("student_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        department = request.POST.get("department", "").strip()
        year = request.POST.get("year", "").strip()

        if not all([
            name,
            email,
            phone,
            department,
            year
        ]):

            messages.error(
                request,
                "Please fill all required fields."
            )

            return redirect(
                "events:register",
                event_id=event_id
            )

        registrations = load_json(
            "registrations.json"
        )

        duplicate = any(
            registration.get("email") == email
            and registration.get("event_id") == event_id
            for registration in registrations
        )

        if duplicate:

            messages.warning(
                request,
                "You are already registered for this event."
            )

            return redirect(
                "events:register",
                event_id=event_id
            )

        new_registration = {
            "student_name": name,
            "email": email,
            "phone": phone,
            "department": department,
            "year": year,
            "event_id": event_id,
            "registered_at": datetime.now().isoformat()
        }

        create_item(
            "registrations.json",
            new_registration
        )

        messages.success(
            request,
            "Registration successful!"
        )

        return redirect(
            "events:events"
        )

    return render(
        request,
        "events/registration.html",
        {
            "event": event
        }
    )


def events_api(request):

    events = load_json("events.json")

    return JsonResponse(
        events,
        safe=False
    )