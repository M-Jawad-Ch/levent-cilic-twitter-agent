from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from agent.models import Tweet, BotStatus
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    bot_status, _ = BotStatus.objects.get_or_create(id=1)

    if request.method == "POST":
        bot_status.is_active = "bot_status" in request.POST
        try:
            interval = int(
                request.POST.get("interval_minutes", bot_status.interval_minutes)
            )
            if interval < 90:
                messages.error(request, "Minimum interval is 90 minutes.")
            else:
                bot_status.interval_minutes = interval
        except ValueError:
            messages.error(request, "Please enter a valid number for interval.")
        bot_status.save()
        return redirect("dashboard")

    tweet_list = Tweet.objects.all()
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get("page")
    tweets = paginator.get_page(page_number)

    return render(
        request,
        "dashboard.html",
        {
            "bot_status": bot_status.is_active,
            "interval_minutes": bot_status.interval_minutes,
            "tweets": tweets,
        },
    )
