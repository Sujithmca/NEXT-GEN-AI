from django.shortcuts import render


def achievements_list(request):
    return render(request, "achievements/achievements.html")
