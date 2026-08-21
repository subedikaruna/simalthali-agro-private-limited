"""
Internal tracking models for the farm.

These link back to core.Goat (your public showcase profiles) via ForeignKey,
so you don't need to maintain goat data twice. This is the data your future
ML models (milk yield prediction, health risk, weight growth, breeding
outcomes) will be trained on — so the more consistently you log here, the
better those predictions will eventually be.
"""

import datetime
from django.db import models
from core.models import Goat

GOAT_GESTATION_DAYS = 150  # average goat gestation length, used to estimate kidding date


class HealthRecord(models.Model):
    goat = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name="health_records")
    date = models.DateField(default=datetime.date.today)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    symptoms = models.TextField(blank=True, help_text="Any observed symptoms, or leave blank if none.")
    is_sick = models.BooleanField(default=False, help_text="Mark true if this goat is currently unwell.")
    vaccinated = models.BooleanField(default=False)
    vaccine_name = models.CharField(max_length=120, blank=True)
    vet_visit = models.BooleanField(default=False)
    vet_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.goat.name} — {self.date}"


class MilkRecord(models.Model):
    goat = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name="milk_records")
    date = models.DateField(default=datetime.date.today)
    yield_liters = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = ("goat", "date")  # one milk entry per goat per day

    def __str__(self):
        return f"{self.goat.name} — {self.date} — {self.yield_liters}L"


class BreedingRecord(models.Model):
    mother = models.ForeignKey(
        Goat, on_delete=models.CASCADE, related_name="breeding_as_mother",
        limit_choices_to={"sex": "F"},
    )
    father = models.ForeignKey(
        Goat, on_delete=models.SET_NULL, related_name="breeding_as_father",
        limit_choices_to={"sex": "M"}, blank=True, null=True,
        help_text="Leave blank if using an external/borrowed sire — use the field below instead.",
    )
    external_sire_name = models.CharField(
        max_length=120, blank=True,
        help_text="Name/ID of sire, only if not one of your own registered goats.",
    )
    mating_date = models.DateField()
    expected_kidding_date = models.DateField(
        blank=True, null=True,
        help_text="Auto-filled from mating date (~150 days) if left blank.",
    )
    actual_kidding_date = models.DateField(blank=True, null=True)
    litter_size = models.PositiveSmallIntegerField(blank=True, null=True)
    had_complications = models.BooleanField(default=False)
    complication_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-mating_date"]

    def __str__(self):
        sire = self.father.name if self.father else (self.external_sire_name or "Unknown sire")
        return f"{self.mother.name} x {sire} — {self.mating_date}"

    def save(self, *args, **kwargs):
        if not self.expected_kidding_date and self.mating_date:
            self.expected_kidding_date = self.mating_date + datetime.timedelta(days=GOAT_GESTATION_DAYS)
        super().save(*args, **kwargs)


class FeedRecord(models.Model):
    date = models.DateField(default=datetime.date.today)
    goat = models.ForeignKey(
        Goat, on_delete=models.CASCADE, related_name="feed_records",
        blank=True, null=True,
        help_text="Leave blank if this feed record is for the whole herd rather than one goat.",
    )
    feed_type = models.CharField(max_length=100, help_text="e.g. hay, grain mix, silage, browse")
    quantity_kg = models.DecimalField(max_digits=6, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        target = self.goat.name if self.goat else "Whole herd"
        return f"{target} — {self.date} — {self.feed_type} ({self.quantity_kg}kg)"
