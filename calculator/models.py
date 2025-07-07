from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Activity(models.Model):   # Czynność
    HAND_CHOICES = [
        ("left", "Lewa ręka"),
        ("right", "Prawa ręka"),
    ]

    vibration_source = models.CharField(max_length=100, blank=True)
    hand = models.CharField(max_length=50, choices=HAND_CHOICES, blank=False, null=False)
    measurement_time = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1), ], default=1)
    round_up_to = models.IntegerField(blank=False, null=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    rounded_ahwx = models.FloatField(blank=True, null=True)
    rounded_ahwy = models.FloatField(blank=True, null=True)
    rounded_ahwz = models.FloatField(blank=True, null=True)
    rounded_vector_summ = models.FloatField(blank=True, null=True)
    partial_exposure = models.FloatField(blank=True, null=True)
    vector_summ_time = models.FloatField(blank=True, null=True)
#for debug
    ahwx = models.FloatField(blank=True, null=True)
    ahwy = models.FloatField(blank=True, null=True)
    ahwz = models.FloatField(blank=True, null=True)
    vector_summ = models.FloatField(blank=True, null=True)
    s_axis_x = models.FloatField(blank=True, null=True)
    s_axis_y = models.FloatField(blank=True, null=True)
    s_axis_z = models.FloatField(blank=True, null=True)
    uprobkj_x = models.FloatField(blank=True, null=True)
    uprobkj_y = models.FloatField(blank=True, null=True)
    uprobkj_z = models.FloatField(blank=True, null=True)
    ucj_x = models.FloatField(blank=True, null=True)
    ucj_y = models.FloatField(blank=True, null=True)
    ucj_z = models.FloatField(blank=True, null=True)
    uhvi = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "activities"
        verbose_name = "activitie"
        ordering = ("-hand", "measurement_time",)

    def __str__(self):
        return f"{self.vibration_source}, {self.hand}/ {self.measurement_time} min."


class Measurement(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="measurements")
    ax = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0),])
    ay = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0),])
    az = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0),])

    class Meta:
        verbose_name_plural = "measurements"

    def __str__(self):
        return f"{self.activity.measurement_time}: {self.ax} {self.ay} {self.az}"


class Indicator(models.Model):

    daily_exposure_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    daily_exposure_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    exposure_30_less_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    exposure_30_less_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    multiplicity_NDN_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    multiplicity_NDN_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    action_threshold_multiplicity_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    action_threshold_multiplicity_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    multiplicity_pregnant_breastfeeding_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    multiplicity_pregnant_breastfeeding_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    multiplicity_young_rh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    multiplicity_young_lh = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
#for debug
    exposure_time_rh = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0),])
    exposure_time_lh = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0),])
    bg20_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0),])
    bg20_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    ba17_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    ba17_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bm9_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bm9_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bg17_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bg17_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq18_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq18_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq17_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq17_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq15_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq15_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h19_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h19_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq21_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bq21_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h20_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h20_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br18_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br18_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br17_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br17_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br15_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    br15_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h21_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h21_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs18_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs18_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs17_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs17_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs15_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    bs15_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h22_l = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])
    h22_r = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), ])

    def __str__(self):
        return f"{self.id}"