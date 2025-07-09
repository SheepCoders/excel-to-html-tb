from django.db.models.aggregates import Sum
from calculator.models import Activity


MULTIPLICITIES_ROUN_UP_TO = 2  # L4
RES_ROUND_UP_TO = 2  # L3
POSSIBLE_VALUE_8H_NDN = 2.8  # BQ19
POSSIBLE_VALUE_8H_WOM = 1  # BR19
POSSIBLE_VALUE_8H_YOUNG = 1  # BS19
POSSIBLE_VALUE_05H_NDN = 11.2  # BQ20
POSSIBLE_VALUE_05H_WOM = 4  # BR20
POSSIBLE_VALUE_05H_YOUNG = 4  # BS20
ACTION_THRESHOLD_VALUE = 2.5  # BQ22
COMBINED_STANDARD_UNCERTAINTY = 13.0  # NIEPEWNOŚĆ_PP D36


def num_of_measur_xyz(activity: Activity, axis: str):  # O19  P19  Q19
    result = None

    if activity.measurements.count() > 0:
        if axis.lower() == "x":
            result = activity.measurements.exclude(ax__isnull=True).count()
        elif axis.lower() == "y":
            result = activity.measurements.exclude(ay__isnull=True).count()
        elif axis.lower() == "z":
            result = activity.measurements.exclude(az__isnull=True).count()
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'")

    return result


def sum_of_square(activity: Activity, axis: str):  # O18  P18  Q18
    summ = 0

    if activity.measurements.count() > 0:
        for measurement in activity.measurements.all():
            if axis.lower() == "x":
                square_x = measurement.ax**2
                summ += square_x
            elif axis.lower() == "y":
                square_y = measurement.ay**2
                summ += square_y
            elif axis.lower() == "z":
                square_z = measurement.az**2
                summ += square_z
            else:
                raise ValueError("Axis must be 'x', 'y', or 'z'")

    return summ


def calculate_ahw(activity: Activity, axis: str):  # E11-16  G11-16
    if activity.measurements.count() > 0:
        ahw = (
            sum_of_square(activity=activity, axis=axis)
            / num_of_measur_xyz(activity=activity, axis=axis)
        ) ** 0.5
        return ahw

    return None


def calculate_vector_summ(activity: Activity):
    summ_of_squares_ahw = 0

    if activity.measurements.count() > 0:
        for axis in ["x", "y", "z"]:
            if calculate_ahw(activity, axis) is not None:
                ahw = calculate_ahw(activity, axis)
                square_ahw = ahw**2
                summ_of_squares_ahw += square_ahw

        vector_summ = summ_of_squares_ahw**0.5

        return vector_summ
    return None


def vector_summ_time(activity: Activity):  # BH11-BH16
    if activity.vector_summ is not None:
        result = (activity.vector_summ**2) * activity.measurement_time
        return result

    return None


def calculate_partial_exposure(activity: Activity):
    if activity.vector_summ is not None:
        partial_exposure = (
            (activity.measurement_time / 480) ** 0.5
        ) * activity.vector_summ
        rounded_partial_exposure = round(partial_exposure, activity.round_up_to)
        return rounded_partial_exposure

    return None


def hand_exposure_time(hand: str):
    total = Activity.objects.filter(hand=hand, measurements__isnull=False).distinct().aggregate(
        total_time=Sum("measurement_time")
    )["total_time"]
    return total if total is not None else None


def num_impact_lt_30(hand: str):  # BM9
    num = Activity.objects.filter(measurement_time__lt=30, hand=hand).count()
    return num


def max_vector_summ_impact_lt_30(hand):  # BG17
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if num_impact_lt_30(hand) > 1:
            vector_sums = [
                activity.vector_summ
                for activity in Activity.objects.filter(
                    measurement_time__lt=30, hand=hand
                )
                if activity.vector_summ is not None
            ]
            max_vector_summ = max(vector_sums) if vector_sums else None
            return round(max_vector_summ, 5)

        elif num_impact_lt_30(hand) == 1:
            activity = Activity.objects.get(hand=hand, measurement_time__lt=30)
            if activity.vector_summ is not None:
                max_vector_summ = activity.vector_summ
                return round(max_vector_summ, 5)
            return None

        elif num_impact_lt_30(hand) < 1:
            return None  # "Nie dot"

    return None


def exceedings_ndn_05h(hand: str):  # BQ18
    exceed = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if num_impact_lt_30(hand) > 0:
            if max_vector_summ_impact_lt_30(hand) is not None:
                not_rounded_exceedings = (
                    max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_NDN
                )
                exceed = round(not_rounded_exceedings, 2)

    return exceed


def value_a8(hand: str):  # BG20
    value = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        print("__________________________________________________")
        if hand_exposure_time(hand) > 0:
            all_vector_summ_time = 0
            for activity in Activity.objects.filter(hand=hand):
                if activity.vector_summ_time is not None:
                    all_vector_summ_time += activity.vector_summ_time

            value = (all_vector_summ_time / 480) ** 0.5

    return value


def exceedings_ndn_8h(hand: str):  # BQ17
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if (
            hand_exposure_time(hand) is not None
            and hand_exposure_time(hand) > 30
            and value_a8(hand) is not None
        ):
            not_rounded_result = value_a8(hand) / POSSIBLE_VALUE_8H_NDN
            result = round(not_rounded_result, 2)

    return result


def num_values_exceeded(hand: str):  # BQ15
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
            result = exceedings_ndn_05h(hand)
        elif num_impact_lt_30(hand) == 0:
            result = exceedings_ndn_8h(hand)
        elif (
            exceedings_ndn_8h(hand) is not None and exceedings_ndn_05h(hand) is not None
        ):
            result = max(exceedings_ndn_8h(hand), exceedings_ndn_05h(hand))

    return result


def multiplicity_ndn(hand: str):  # H19
    multiplicity = None

    if num_values_exceeded(hand=hand) is not None:
        multiplicity = round(num_values_exceeded(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return multiplicity


def numb_threshold_values_exceeded(hand: str):  # BQ21
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if value_a8(hand=hand) is not None:
            result = round((value_a8(hand=hand) / ACTION_THRESHOLD_VALUE), 2)

    return result


def action_threshold_multiplicity(hand: str):  # H20
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if numb_threshold_values_exceeded(hand=hand) is not None:
            result = round(
                numb_threshold_values_exceeded(hand=hand), MULTIPLICITIES_ROUN_UP_TO
            )

    return result


def exceedings_ndn_05h_women(hand: str):  # BR18
    exceed = None

    if num_impact_lt_30(hand) > 0:
        if max_vector_summ_impact_lt_30(hand) is not None:
            not_rounded_exceedings = (
                max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_WOM
            )
            exceed = round(not_rounded_exceedings, 2)
    return exceed


def exceedings_ndn_8h_women(hand: str):  # BR17
    result = None

    if (
        hand_exposure_time(hand) is not None
        and hand_exposure_time(hand) > 30
        and value_a8(hand) is not None
    ):
        not_rounded_result = value_a8(hand) / POSSIBLE_VALUE_8H_WOM
        result = round(not_rounded_result, 2)

    return result


def num_values_exceeded_pregn_breast(hand: str):  # BR15
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
        result = exceedings_ndn_05h_women(hand)
    elif num_impact_lt_30(hand) == 0:
        result = exceedings_ndn_8h_women(hand)
    elif (
        exceedings_ndn_8h_women(hand) is not None
        and exceedings_ndn_05h_women(hand) is not None
    ):
        result = max(exceedings_ndn_8h_women(hand), exceedings_ndn_05h_women(hand))

    return result


def multiplicity_pregnant_breastfeeding(hand: str):  # H21
    result = None

    if num_values_exceeded_pregn_breast(hand=hand) is not None:
        result = round(
            num_values_exceeded_pregn_breast(hand=hand), MULTIPLICITIES_ROUN_UP_TO
        )

    return result


def exceedings_ndn_05h_young(hand: str):  # BS18
    exceed = None

    if num_impact_lt_30(hand) > 0:
        if max_vector_summ_impact_lt_30(hand) is not None:
            not_rounded_exceedings = (
                max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_YOUNG
            )
            exceed = round(not_rounded_exceedings, 2)
    return exceed


def exceedings_ndn_8h_young(hand: str):  # BS17
    result = None

    if (
        hand_exposure_time(hand) is not None
        and hand_exposure_time(hand) > 30
        and value_a8(hand) is not None
    ):
        not_rounded_result = value_a8(hand) / POSSIBLE_VALUE_8H_YOUNG
        result = round(not_rounded_result, 2)
    #
    return result


def num_values_exceeded_young(hand: str):  # BS15
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
        result = exceedings_ndn_05h_young(hand)
    elif num_impact_lt_30(hand) == 0:
        result = exceedings_ndn_8h_young(hand)
    elif (
        exceedings_ndn_8h_young(hand) is not None
        and exceedings_ndn_05h_young(hand) is not None
    ):
        result = max(exceedings_ndn_8h_young(hand), exceedings_ndn_05h_young(hand))

    return result


def multiplicity_young(hand: str):  # H22
    result = None

    if num_values_exceeded_young(hand=hand) is not None:
        result = round(num_values_exceeded_young(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return result


def s(activity: Activity, axis: str):  # O20
    s = None

    if activity.measurements.count() > 1 and activity.measurement_time is not None:
        ahw_axis = calculate_ahw(activity=activity, axis=axis)
        sum_of_square_stdev = 0

        for measurement in activity.measurements.all():
            if axis.lower() == "x":
                square_stdev = (measurement.ax - ahw_axis) ** 2
                sum_of_square_stdev += square_stdev
            elif axis.lower() == "y":
                square_stdev = (measurement.ay - ahw_axis) ** 2
                sum_of_square_stdev += square_stdev
            elif axis.lower() == "z":
                square_stdev = (measurement.az - ahw_axis) ** 2
                sum_of_square_stdev += square_stdev

        s = round((sum_of_square_stdev / (activity.measurements.count() - 1)) ** 0.5, 5)

    return s


def uprobkj(activity: Activity, axis: str):  # O21
    if activity.measurement_time is not None:

        if activity.measurements.count() > 1:
            if axis.lower() == "x":
                uprobkj = activity.s_axis_x / (
                    (activity.measurements.count() ** 0.5) * activity.ahwx
                )
            elif axis.lower() == "y":
                uprobkj = activity.s_axis_y / (
                    (activity.measurements.count() ** 0.5) * activity.ahwy
                )
            elif axis.lower() == "z":
                uprobkj = activity.s_axis_z / (
                    (activity.measurements.count() ** 0.5) * activity.ahwz
                )
            return round(uprobkj, 5)

        if activity.measurements.count() == 1:
            return 0

    return None


def ucj(activity: Activity, axis: str):  # O22
    ucj = None

    if activity.measurement_time is not None:
        if axis.lower() == "x":
            ucj = (
                activity.uprobkj_x**2 + (COMBINED_STANDARD_UNCERTAINTY / 100) ** 2
            ) ** 0.5
        elif axis.lower() == "y":
            ucj = (
                activity.uprobkj_y**2 + (COMBINED_STANDARD_UNCERTAINTY / 100) ** 2
            ) ** 0.5
        elif axis.lower() == "z":
            ucj = (
                activity.uprobkj_z**2 + (COMBINED_STANDARD_UNCERTAINTY / 100) ** 2
            ) ** 0.5

        return round(ucj, 5)

    return ucj


def uhvi(activity: Activity):  # BG11 = #R22
    if activity.measurements is not None:
        if activity.vector_summ is not None and activity.vector_summ > 0:
            activity.uhvi = round(
                (
                    (
                        (
                            ((activity.ucj_x * (activity.ahwx**2)) ** 2)
                            + ((activity.ucj_y * (activity.ahwy**2)) ** 2)
                            + ((activity.ucj_z * (activity.ahwz**2)) ** 2)
                        )
                    )
                    / activity.vector_summ**2
                )
                ** 0.5,
                5,
            )

            return activity.uhvi

    return None


def cai(activity: Activity):  # BI11
    if (
        activity.measurement_time is not None and value_a8("right") is not None
    ):  # ??? right(should be activity.hand)
        if value_a8("right") > 0:
            cai = (
                activity.measurement_time
                * activity.vector_summ
                / (480 * value_a8("right"))
            )
            return cai

    return None


def caiuci2(activity: Activity):  # BJ11-16
    if activity.measurement_time is not None:
        if activity.uhvi and activity.cai:
            return (activity.uhvi * activity.cai) ** 2

    return None


def uti_rh(activity: Activity):  # BB11 - BB16
    if Activity.objects.filter(hand="right") is not None:
        if activity.measurement_time is not None:
            return 0
            ## Q1 -Q3 how works?
    return None


def uti_lh(activity: Activity):  # BB11 - BB16
    if Activity.objects.filter(hand="left") is not None:
        if activity.measurement_time is not None:
            return 0
            ## Q1 -Q3 how works?
    return None


def cti(activity: Activity):  # BK11 -BK16   BK36 - BK41
    if activity.measurement_time is not None and value_a8("right") is not None:
        if value_a8("right") > 0:
            return activity.vector_summ**2 / (
                2 * 480 * value_a8("right")
            )  # ?? "right"?

    return None


def ctiuti2(activity: Activity):  # BL11 -BL16
    if activity.measurement_time is not None:
        if activity.hand.lower() == "right":
            if activity.uti_lh and activity.cti:
                return (activity.uti_lh * activity.cti) ** 2

    return None


def uca8(hand: str):  # BG21
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        sum_of_caiuci2 = 0
        sum_of_ctiuti2 = 0

        for activity in Activity.objects.filter(hand=hand):
            if activity.caiuci2 is not None:
                sum_of_caiuci2 += activity.caiuci2
            if activity.ctiuti2 is not None:
                sum_of_ctiuti2 += activity.ctiuti2

        return (sum_of_caiuci2 + sum_of_ctiuti2) ** 0.5
    return None


def _2xuca8(hand: str):  # BG22
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if uca8(hand=hand) is not None:
            return 2 * uca8(hand=hand)
    return None


def daily_exposure(hand: str):  # H17 H42
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():

        if (
            hand_exposure_time(hand=hand) is not None
            and hand_exposure_time(hand=hand) > 30
        ):
            if value_a8(hand) is not None and _2xuca8(hand=hand) is not None:
                first_value = round(value_a8(hand=hand), RES_ROUND_UP_TO)
                second_value = round(_2xuca8(hand=hand), RES_ROUND_UP_TO)
                return f"{first_value} ± {second_value}"

        return f"Nie dotyczy"
    return None


def uahv(activity: Activity):  # BN11 - BN16
    if activity.measurement_time is not None and activity.measurement_time <= 30:
        return activity.uhvi
    return None


def ucahvmax(hand: str):  # BG18
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if num_impact_lt_30(hand) > 1:
            uahv_sums = [
                activity.uahv
                for activity in Activity.objects.filter(
                    measurement_time__lt=30, hand=hand
                )
                if activity.uahv is not None
            ]
            max_uahv = max(uahv_sums) if uahv_sums else None
            return round(max_uahv, 5)

        elif num_impact_lt_30(hand) == 1:
            activity = Activity.objects.get(hand=hand, measurement_time__lt=30)
            if activity.uahv is not None:
                max_uahv = activity.uahv
                return round(max_uahv, 5)
            return None

        elif num_impact_lt_30(hand) < 1:
            return None  # "Nie dot"

    return None


# BG19 = 2 * BG18


def exposure_30_less(hand: str):  # H18
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if Activity.objects.filter(measurement_time__lt=30, hand=hand).exists():
            if max_vector_summ_impact_lt_30(hand=hand) and ucahvmax(hand=hand):
                return f"{round(max_vector_summ_impact_lt_30(hand=hand), 2)} ± {round(ucahvmax(hand=hand) * 2, 2)}"

        return "Nie dotyczy"
    return None
