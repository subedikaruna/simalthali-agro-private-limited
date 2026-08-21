import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg
from django.shortcuts import render
from core.models import Goat
from .models import HealthRecord, MilkRecord, BreedingRecord, FeedRecord


@staff_member_required
def dashboard_home(request):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    month_from_now = today + datetime.timedelta(days=30)

    total_goats = Goat.objects.count()

    sick_goats = (
        HealthRecord.objects.filter(is_sick=True, date__gte=week_ago)
        .values("goat__name").distinct()
    )

    week_milk = MilkRecord.objects.filter(date__gte=week_ago).aggregate(
        total=Sum("yield_liters"), avg=Avg("yield_liters")
    )

    upcoming_kiddings = (
        BreedingRecord.objects.filter(
            actual_kidding_date__isnull=True,
            expected_kidding_date__gte=today,
            expected_kidding_date__lte=month_from_now,
        ).select_related("mother", "father")
    )

    recent_health = HealthRecord.objects.select_related("goat").order_by("-date")[:5]
    recent_milk = MilkRecord.objects.select_related("goat").order_by("-date")[:5]

    month_feed_cost = FeedRecord.objects.filter(
        date__gte=today.replace(day=1)
    ).aggregate(total=Sum("cost"))["total"]

    context = {
        "total_goats": total_goats,
        "sick_goats": sick_goats,
        "week_milk_total": week_milk["total"] or 0,
        "week_milk_avg": week_milk["avg"] or 0,
        "upcoming_kiddings": upcoming_kiddings,
        "recent_health": recent_health,
        "recent_milk": recent_milk,
        "month_feed_cost": month_feed_cost or 0,
    }
    return render(request, "farmapp/dashboard.html", context)


@staff_member_required
def goat_lookup(request):
    """
    Type an ear tag number in, get back everything known about that goat:
    lineage (mother/father), breed, age, latest health status, and a milk
    summary — all in one place instead of hunting through the admin panel.
    """
    tag = request.GET.get("tag", "").strip()
    goat = None
    not_found = False
    latest_health = None
    milk_last_30_days = None
    upcoming_breeding = None
    today = datetime.date.today()

    if tag:
        try:
            goat = Goat.objects.select_related("breed", "mother", "father").get(
                ear_tag_number__iexact=tag
            )
        except Goat.DoesNotExist:
            not_found = True

    if goat:
        latest_health = goat.health_records.order_by("-date").first()

        milk_last_30_days = goat.milk_records.filter(
            date__gte=today - datetime.timedelta(days=30)
        ).aggregate(total=Sum("yield_liters"))["total"] or 0

        if goat.sex == "F":
            upcoming_breeding = (
                BreedingRecord.objects.filter(mother=goat, actual_kidding_date__isnull=True)
                .order_by("expected_kidding_date").first()
            )

        if goat.date_of_birth:
            age_days = (today - goat.date_of_birth).days
            goat.age_display = (
                f"{age_days // 365} yr {(age_days % 365) // 30} mo" if age_days >= 365
                else f"{age_days // 30} mo" if age_days >= 30
                else f"{age_days} days"
            )
        else:
            goat.age_display = None

    context = {
        "tag": tag,
        "goat": goat,
        "not_found": not_found,
        "latest_health": latest_health,
        "milk_last_30_days": milk_last_30_days,
        "upcoming_breeding": upcoming_breeding,
    }
    return render(request, "farmapp/lookup.html", context)