from django.urls import reverse_lazy
from django.views import generic
from .calculations import (
    calculate_ahw,
    calculate_vector_summ,
    calculate_partial_exposure,
    hand_exposure_time,
    vector_summ_time,
    multiplicity_ndn,
    action_threshold_multiplicity,
    multiplicity_pregnant_breastfeeding,
    multiplicity_young,
    value_a8,
    num_impact_lt_30,
    max_vector_summ_impact_lt_30,
    exceedings_ndn_05h,
    exceedings_ndn_8h,
    num_values_exceeded,
    numb_threshold_values_exceeded,
    exceedings_ndn_05h_women,
    exceedings_ndn_8h_women,
    num_values_exceeded_pregn_breast,
    exceedings_ndn_05h_young,
    exceedings_ndn_8h_young,
    num_values_exceeded_young,
    s,
    uprobkj,
    ucj,
    uhvi,
    cai,
    caiuci2,
    uti_rh,
    uti_lh,
    cti,
    ctiuti2,
    uca8,
    _2xuca8,
    daily_exposure,
    uahv,
    ucahvmax,
    exposure_30_less,
)
from .models import Activity, Measurement, Indicator


class CombinedActivityIndicatorView(generic.ListView):
    model = Activity
    context_object_name = "activity_list"
    template_name = "calculator/index.html"
    queryset = Activity.objects.prefetch_related("measurements").all()
    # paginate_by = 5

    @staticmethod
    def calculate_vibration_data(activity: Activity):
            activity.ahwx = calculate_ahw(activity, "x")
            activity.ahwy = calculate_ahw(activity, "y")
            activity.ahwz = calculate_ahw(activity, "z")
            activity.vector_summ = calculate_vector_summ(activity)
            activity.rounded_ahwx = round(
                calculate_ahw(activity, "x"), activity.round_up_to
            )
            activity.rounded_ahwy = round(
                calculate_ahw(activity, "y"), activity.round_up_to
            )
            activity.rounded_ahwz = round(
                calculate_ahw(activity, "z"), activity.round_up_to
            )
            activity.rounded_vector_summ = round(
                activity.vector_summ, activity.round_up_to
            )
            activity.partial_exposure = calculate_partial_exposure(activity)
            activity.vector_summ_time = vector_summ_time(activity)
            # for debug
            activity.s_axis_x = s(activity, "x")
            activity.s_axis_y = s(activity, "y")
            activity.s_axis_z = s(activity, "z")
            activity.uprobkj_x = uprobkj(activity, "x")
            activity.uprobkj_y = uprobkj(activity, "y")
            activity.uprobkj_z = uprobkj(activity, "z")
            activity.ucj_x = ucj(activity, "x")
            activity.ucj_y = ucj(activity, "y")
            activity.ucj_z = ucj(activity, "z")
            activity.uhvi = uhvi(activity)
            activity.cai = cai(activity)
            activity.caiuci2 = caiuci2(activity)
            activity.uti_rh = uti_rh(activity)
            activity.uti_lh = uti_lh(activity)
            activity.cti = cti(activity)
            activity.ctiuti2 = ctiuti2(activity)
            activity.caiuci2 = caiuci2(activity)
            activity.uahv = uahv(activity)

            activity.save()


    @staticmethod
    def reset_vibration_data(activity: Activity):
            activity.ahwx = None
            activity.ahwy = None
            activity.ahwz = None
            activity.vector_summ = None
            activity.rounded_ahwx = None
            activity.rounded_ahwy = None
            activity.rounded_ahwz = None
            activity.rounded_vector_summ = None
            activity.partial_exposure = None
            activity.vector_summ_time = None
            # for debug
            activity.s_axis_x = None
            activity.s_axis_y = None
            activity.s_axis_z = None
            activity.uprobkj_x = None
            activity.uprobkj_y = None
            activity.uprobkj_z = None
            activity.ucj_x = None
            activity.ucj_y = None
            activity.ucj_z = None
            activity.uhvi = None
            activity.cai = None
            activity.caiuci2 = None
            activity.uti_rh = None
            activity.uti_lh = None
            activity.cti = None
            activity.ctiuti2 = None
            activity.caiuci2 = None
            activity.uahv = None

            activity.save()


    @staticmethod
    def calculate_indicator_right_hand(indicator: Indicator, hand: str):
        indicator.exposure_time_rh = hand_exposure_time("right")
        indicator.multiplicity_NDN_rh = multiplicity_ndn("right")
        indicator.action_threshold_multiplicity_rh = (
            action_threshold_multiplicity("right")
        )
        indicator.multiplicity_pregnant_breastfeeding_rh = (
            multiplicity_pregnant_breastfeeding("right")
        )
        indicator.multiplicity_young_rh = multiplicity_young("right")
        indicator.daily_exposure_rh = daily_exposure("right")
        # for debug
        indicator.bg20_r = value_a8("right")
        indicator.ba17_r = hand_exposure_time("right")
        indicator.bm9_r = num_impact_lt_30("right")
        indicator.bg17_r = max_vector_summ_impact_lt_30("right")
        indicator.bq18_r = exceedings_ndn_05h("right")
        indicator.bq17_r = exceedings_ndn_8h("right")
        indicator.bq15_r = num_values_exceeded("right")
        indicator.h19_r = multiplicity_ndn("right")
        indicator.bq21_r = numb_threshold_values_exceeded("right")
        indicator.h20_r = action_threshold_multiplicity("right")
        indicator.br18_r = exceedings_ndn_05h_women("right")
        indicator.br17_r = exceedings_ndn_8h_women("right")
        indicator.br15_r = num_values_exceeded_pregn_breast("right")
        indicator.h21_r = multiplicity_pregnant_breastfeeding("right")
        indicator.bs18_r = exceedings_ndn_05h_young("right")
        indicator.bs17_r = exceedings_ndn_8h_young("right")
        indicator.bs15_r = num_values_exceeded_young("right")
        indicator.uca_8_r = uca8("right")
        indicator._2xuca8_r = _2xuca8("right")
        indicator.h22_r = multiplicity_young("right")
        indicator.ucahvmax_r = ucahvmax("right")
        indicator.exposure_30_less_rh = exposure_30_less("right")

        indicator.save()


    @staticmethod
    def calculate_indicator_left_hand(indicator: Indicator, hand: str):
        indicator.exposure_time_lh = hand_exposure_time("left")
        indicator.multiplicity_NDN_lh = multiplicity_ndn("left")
        indicator.action_threshold_multiplicity_lh = (
            action_threshold_multiplicity("left")
        )
        indicator.multiplicity_pregnant_breastfeeding_lh = (
            multiplicity_pregnant_breastfeeding("left")
        )
        indicator.multiplicity_young_lh = multiplicity_young("left")
        indicator.daily_exposure_lh = daily_exposure("left")
        # for debug
        indicator.bg20_l = value_a8("left")
        indicator.ba17_l = hand_exposure_time("left")
        indicator.bm9_l = num_impact_lt_30("left")
        indicator.bg17_l = max_vector_summ_impact_lt_30("left")
        indicator.bq18_l = exceedings_ndn_05h("left")
        indicator.bq17_l = exceedings_ndn_8h("left")
        indicator.bq15_l = num_values_exceeded("left")
        indicator.h19_l = multiplicity_ndn("left")
        indicator.bq21_l = numb_threshold_values_exceeded("left")
        indicator.h20_l = action_threshold_multiplicity("left")
        indicator.br18_l = exceedings_ndn_05h_women("left")
        indicator.br17_l = exceedings_ndn_8h_women("left")
        indicator.br15_l = num_values_exceeded_pregn_breast("left")
        indicator.h21_l = multiplicity_pregnant_breastfeeding("left")
        indicator.bs18_l = exceedings_ndn_05h_young("left")
        indicator.bs17_l = exceedings_ndn_8h_young("left")
        indicator.bs15_l = num_values_exceeded_young("left")
        indicator.h22_l = multiplicity_young("left")
        indicator.uca_8_l = uca8("left")
        indicator._2xuca8_l = _2xuca8("left")
        indicator.ucahvmax_l = ucahvmax("left")
        indicator.exposure_30_less_lh = exposure_30_less("left")

        indicator.save()


    @staticmethod
    def reset_indicator_right_hand(indicator: Indicator):
        indicator.exposure_time_rh = None
        indicator.multiplicity_NDN_rh = None
        indicator.action_threshold_multiplicity_rh = None
        indicator.multiplicity_pregnant_breastfeeding_rh = None
        indicator.multiplicity_young_rh = None
        indicator.daily_exposure_rh = None
        # for debug
        indicator.bg20_r = None
        indicator.ba17_r = None
        indicator.bm9_r = None
        indicator.bg17_r = None
        indicator.bq18_r = None
        indicator.bq17_r = None
        indicator.bq15_r = None
        indicator.h19_r = None
        indicator.bq21_r = None
        indicator.h20_r = None
        indicator.br18_r = None
        indicator.br17_r = None
        indicator.br15_r = None
        indicator.h21_r = None
        indicator.bs18_r = None
        indicator.bs17_r = None
        indicator.bs15_r = None
        indicator.h22_r = None
        indicator.ucahvmax_r = None
        indicator.exposure_30_less_rh = None
        indicator.uca_8_r = None
        indicator._2xuca8_r = None

        indicator.save()


    @staticmethod
    def reset_indicator_left_hand(indicator: Indicator):
        indicator.exposure_time_lh = None
        indicator.multiplicity_NDN_lh = None
        indicator.action_threshold_multiplicity_lh = None
        indicator.multiplicity_pregnant_breastfeeding_lh = None
        indicator.multiplicity_young_lh = None
        indicator.daily_exposure_lh = None
        # for debug
        indicator.bg20_l = None
        indicator.ba17_l = None
        indicator.bm9_l = None
        indicator.bg17_l = None
        indicator.bq18_l = None
        indicator.bq17_l = None
        indicator.bq15_l = None
        indicator.h19_l = None
        indicator.bq21_l = None
        indicator.h20_l = None
        indicator.br18_l = None
        indicator.br17_l = None
        indicator.br15_l = None
        indicator.h21_l = None
        indicator.bs18_l = None
        indicator.bs17_l = None
        indicator.bs15_l = None
        indicator.h22_l = None
        indicator.ucahvmax_l = None
        indicator.exposure_30_less_lh = None
        indicator.uca_8_l = None
        indicator._2xuca8_l = None

        indicator.save()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CombinedActivityIndicatorView, self).get_context_data(**kwargs)
        context["indicator_list"] = Indicator.objects.all()

        if Indicator.objects.count() == 0:
            indicator = Indicator.objects.create()
        else: indicator = Indicator.objects.all()[0]

        if Activity.objects.filter(measurements__isnull=False).exists():
            for activity in Activity.objects.filter(measurements__isnull=False):
                self.calculate_vibration_data(activity=activity)
        if Activity.objects.filter(measurements__isnull=True).exists():
            for activity in Activity.objects.filter(measurements__isnull=True):
                self.reset_vibration_data(activity=activity)

        if Activity.objects.filter(measurements__isnull=False, hand="right").exists():
            self.calculate_indicator_right_hand(indicator=indicator, hand="right")
        elif Activity.objects.filter(measurements__isnull=True, hand="right").exists():
            self.reset_indicator_right_hand(indicator=indicator)

        if Activity.objects.filter(measurements__isnull=False, hand="left").exists():
            self.calculate_indicator_left_hand(indicator=indicator, hand="left")
        elif Activity.objects.filter(measurements__isnull=True, hand="left").exists():
            self.reset_indicator_left_hand(indicator=indicator)

        return context


class ActivityCreateView(generic.CreateView):
    model = Activity
    fields = ("vibration_source", "measurement_time", "hand", "round_up_to")
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/activity_form.html"


class ActivityUpdateView(generic.UpdateView):
    model = Activity
    fields = ("vibration_source", "measurement_time", "hand", "round_up_to")
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/activity_form.html"


class ActivityDeleteView(generic.DeleteView):
    model = Activity
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/activity_confirm_delete.html"


class MeasurementCreateView(generic.CreateView):
    model = Measurement
    fields = ("activity", "ax", "ay", "az")
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/measurement_form.html"


class MeasurementUpdateView(generic.UpdateView):
    model = Measurement
    fields = ("activity", "ax", "ay", "az")
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/measurement_form.html"


class MeasurementDeleteView(generic.DeleteView):
    model = Measurement
    success_url = reverse_lazy("calculator:activity_list")
    template_name = "calculator/measurement_confirm_delete.html"
