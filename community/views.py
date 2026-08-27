from datetime import datetime, timezone

from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import login_required_custom
from accounts.utils import load_members, update_member


def home(request):
    joined = bool(request.session.get("joined_club"))
    return render(
        request,
        "community/join_club.html",
        {"joined": joined},
    )


@login_required_custom
def join_club(request):
    member = next(
        (
            item for item in load_members()
            if str(item.get("id")) == str(request.session.get("member_id"))
        ),
        None,
    )
    if not member:
        request.session.flush()
        return redirect("accounts:login")

    joined = bool(member.get("club_member", False))

    if request.method == "POST":
        member = update_member(
            member["id"],
            {
                "club_member": True,
                "joined_at": member.get("joined_at") or datetime.now(timezone.utc).isoformat(),
            },
        )
        request.session["joined_club"] = True
        messages.success(
            request,
            "You have successfully joined the NextGenAI club.",
        )
        return redirect("community:join")

    return render(
        request,
        "community/join_club.html",
        {"joined": joined, "member": member},
    )
