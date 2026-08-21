from django.contrib import admin
from .models import HealthRecord, MilkRecord, BreedingRecord, FeedRecord


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("goat", "date", "weight_kg", "is_sick", "vet_visit")
    list_filter = ("is_sick", "vet_visit", "vaccinated", "date")
    search_fields = ("goat__name", "symptoms")
    autocomplete_fields = ["goat"]
    date_hierarchy = "date"


@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    list_display = ("goat", "date", "yield_liters")
    list_filter = ("date",)
    search_fields = ("goat__name",)
    autocomplete_fields = ["goat"]
    date_hierarchy = "date"


@admin.register(BreedingRecord)
class BreedingRecordAdmin(admin.ModelAdmin):
    list_display = ("mother", "father", "mating_date", "expected_kidding_date", "actual_kidding_date", "litter_size")
    list_filter = ("had_complications",)
    search_fields = ("mother__name", "father__name", "external_sire_name")
    autocomplete_fields = ["mother", "father"]
    date_hierarchy = "mating_date"


@admin.register(FeedRecord)
class FeedRecordAdmin(admin.ModelAdmin):
    list_display = ("date", "goat", "feed_type", "quantity_kg", "cost")
    list_filter = ("feed_type", "date")
    search_fields = ("feed_type", "goat__name")
    autocomplete_fields = ["goat"]
    date_hierarchy = "date"
