from django.contrib import admin
from calculator.models import *


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("vibration_source", "measurement_time", "hand", "round_up_to")
    list_filter = ("vibration_source", "measurement_time", "hand")
    search_fields = ("vibration_source",)


@admin.register(Measurement)
class MeasurementTypeAdmin(admin.ModelAdmin):
    list_display = ("ax", "ay", "az")


@admin.register(Indicator)
class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = (
        "daily_exposure_rh",
        "daily_exposure_lh",
        "exposure_30_less_rh",
        "exposure_30_less_lh",
        "multiplicity_NDN_rh",
        "multiplicity_NDN_lh",
        "action_threshold_multiplicity_rh",
        "action_threshold_multiplicity_lh",
        "multiplicity_pregnant_breastfeeding_rh",
        "multiplicity_pregnant_breastfeeding_lh",
        "multiplicity_young_rh",
        "multiplicity_young_lh",
        "exposure_time_rh",
        "exposure_time_lh",
    )
