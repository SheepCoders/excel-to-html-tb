from calculator.models import Activity, Indicator


MULTIPLICITIES_ROUN_UP_TO = 2       #L4
RES_ROUND_UP_TO = 2                 #L3

POSSIBLE_VALUE_8H_NDN = 2.8         #BQ19
POSSIBLE_VALUE_8H_WOM = 1           #BR19
POSSIBLE_VALUE_8H_YOUNG = 1         #BS19
POSSIBLE_VALUE_05H_NDN = 11.2       #BQ20
POSSIBLE_VALUE_05H_WOM = 4          #BR20
POSSIBLE_VALUE_05H_YOUNG = 4        #BS20

ACTION_THRESHOLD_VALUE = 2.5        #BQ22

COMBINED_STANDARD_UNCERTAINTY = 13.0    #NIEPEWNOŚĆ_PP D36


def num_of_measur_xyz(activity: Activity, axis: str):                             #O19  P19  Q19
    result = None

    if activity.measurements.count() > 0:
        if axis.lower() == "x":
            result = activity.measurements.exclude(ax__isnull=True).count()
        elif axis.lower() == 'y':
            result = activity.measurements.exclude(ay__isnull=True).count()
        elif axis.lower() == 'z':
            result = activity.measurements.exclude(az__isnull=True).count()
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'")

    return result


def sum_of_square(activity: Activity, axis: str):                                         #O18  P18  Q18
    summ = 0

    if activity.measurements.count() > 0:
        for measurement in activity.measurements.all():
            if axis.lower() == "x":
                square_x = measurement.ax ** 2
                summ += square_x
            elif axis.lower() == "y":
                square_y = measurement.ay ** 2
                summ += square_y
            elif axis.lower() == "z":
                square_z = measurement.az ** 2
                summ += square_z
            else:
                raise ValueError("Axis must be 'x', 'y', or 'z'")

    return summ


def calculate_ahw(activity: Activity, axis: str):                                               #E11-16  G11-16
    if activity.measurements.count() > 0:
        ahw = (sum_of_square(activity=activity, axis=axis) / num_of_measur_xyz(activity=activity, axis=axis)) ** 0.5

        return ahw
    return None


def calculate_vector_summ(activity: Activity):
    summ_of_squares_ahw = 0

    if activity.measurements.count() > 0:
        for axis in ["x", "y", "z"]:
            if calculate_ahw(activity, axis) is not None:
                ahw = calculate_ahw(activity, axis)
                square_ahw = ahw ** 2
                summ_of_squares_ahw += square_ahw

        vector_summ = summ_of_squares_ahw ** 0.5

        return vector_summ
    return None


def vector_summ_time(activity: Activity):                                                          #BH11-BH16
    if activity.vector_summ is not None:
        result = (activity.vector_summ ** 2) * activity.measurement_time
        return result

    return None


def calculate_partial_exposure(activity: Activity):
    if activity.vector_summ is not None:
        partial_exposure = ((activity.measurement_time / 480) ** 0.5) * activity.vector_summ
        rounded_partial_exposure = round(partial_exposure, activity.round_up_to)
        return rounded_partial_exposure

    return None


def hand_exposure_time(hand: str):                                                         #BA17
    hand_exposure = 0

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        for activity in Activity.objects.all():
            if activity.hand == hand:
                if activity.measurement_time is not None:
                    hand_exposure += activity.measurement_time

        return hand_exposure
    return None


def num_impact_lt_30(hand: str):                                                              #BM9
    num = Activity.objects.filter(measurement_time__lt=30, hand=hand).count()
    return num


def max_vector_summ_impact_lt_30(hand):                                                       #BG17
    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if num_impact_lt_30(hand) > 1:
            vector_sums = [
                activity.vector_summ for activity in Activity.objects.filter(measurement_time__lt=30, hand=hand)
                if activity.vector_summ is not None
            ]
            max_vector_summ = max(vector_sums) if vector_sums else None
            return round(max_vector_summ, 5)

        elif num_impact_lt_30(hand) == 1:
            activity = Activity.objects.get(hand=hand, measurement_time__lt=30)
            max_vector_summ = activity.vector_summ if activity.vector_summ is not None else None
            return round(max_vector_summ, 5)

        elif num_impact_lt_30(hand) < 1:
            return None   #"Nie dot"

    return None

def exceedings_ndn_05h(hand: str):                                                                #BQ18
    exceed = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if num_impact_lt_30(hand) > 0:
            if max_vector_summ_impact_lt_30(hand) is not None:
                not_rounded_exceedings = max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_NDN
                exceed = round(not_rounded_exceedings, 2)

    return exceed


def value_a8(hand: str):                                                                        #BG20
    value = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if hand_exposure_time(hand) > 0:
            all_vector_summ_time = 0
            for activity in Activity.objects.filter(hand=hand):
                if activity.vector_summ_time is not None:
                    all_vector_summ_time += activity.vector_summ_time

            value = (all_vector_summ_time / 480) ** 0.5

    return value


def exceedings_ndn_8h(hand: str):                                                                #BQ17
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if hand_exposure_time(hand) is not None and hand_exposure_time(hand) > 30 and value_a8(hand) is not None:
            not_rounded_result = (value_a8(hand) / POSSIBLE_VALUE_8H_NDN)
            result = round(not_rounded_result, 2)

    return result
#
#
def num_values_exceeded(hand: str):                                                               #BQ15
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
            result = exceedings_ndn_05h(hand)
        elif num_impact_lt_30(hand) == 0:
            result = exceedings_ndn_8h(hand)
        elif exceedings_ndn_8h(hand) is not None and exceedings_ndn_05h(hand) is not None:
            result = max(exceedings_ndn_8h(hand), exceedings_ndn_05h(hand))

    return result

def multiplicity_ndn(hand: str):                                                                     #H19
    multiplicity = None

    if num_values_exceeded(hand=hand) is not None:
        multiplicity = round(num_values_exceeded(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return multiplicity


def numb_threshold_values_exceeded(hand:str):                                                        #BQ21
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if value_a8(hand=hand) is not None:
            result = round((value_a8(hand=hand) / ACTION_THRESHOLD_VALUE), 2)

    return result


def action_threshold_multiplicity(hand: str):                                                             #H20
    result = None

    if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
        if numb_threshold_values_exceeded(hand=hand) is not None:
            result = round(numb_threshold_values_exceeded(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return result


def exceedings_ndn_05h_women(hand: str):                                                                    #BR18
    exceed = None

    if num_impact_lt_30(hand) > 0:
        if max_vector_summ_impact_lt_30(hand) is not None:
            not_rounded_exceedings = max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_WOM
            exceed = round(not_rounded_exceedings, 2)
    return exceed


def exceedings_ndn_8h_women(hand: str):                                                                    #BR17
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) > 30 and value_a8(hand) is not None:
        not_rounded_result = (value_a8(hand) / POSSIBLE_VALUE_8H_WOM)
        result = round(not_rounded_result, 2)

    return result


def num_values_exceeded_pregn_breast(hand: str):                                                      # BR15
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
        result = exceedings_ndn_05h_women(hand)
    elif num_impact_lt_30(hand) == 0:
        result = exceedings_ndn_8h_women(hand)
    elif exceedings_ndn_8h_women(hand) is not None and exceedings_ndn_05h_women(hand) is not None:
        result = max(exceedings_ndn_8h_women(hand), exceedings_ndn_05h_women(hand))

    return result


def multiplicity_pregnant_breastfeeding(hand: str):                                                 #H21
    result = None

    if num_values_exceeded_pregn_breast(hand=hand) is not None:
        result = round(num_values_exceeded_pregn_breast(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return result


def exceedings_ndn_05h_young(hand: str):                                                                    #BS18
    exceed = None

    if num_impact_lt_30(hand) > 0:
        if max_vector_summ_impact_lt_30(hand) is not None:
            not_rounded_exceedings = max_vector_summ_impact_lt_30(hand) / POSSIBLE_VALUE_05H_YOUNG
            exceed = round(not_rounded_exceedings, 2)
    return exceed


def exceedings_ndn_8h_young(hand: str):                                                                    #BS17
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) > 30 and value_a8(hand) is not None:
        not_rounded_result = (value_a8(hand) / POSSIBLE_VALUE_8H_YOUNG)
        result = round(not_rounded_result, 2)
    #
    return result


def num_values_exceeded_young(hand: str):                                                                # BS15
    result = None

    if hand_exposure_time(hand) is not None and hand_exposure_time(hand) <= 30:
        result = exceedings_ndn_05h_young(hand)
    elif num_impact_lt_30(hand) == 0:
        result = exceedings_ndn_8h_young(hand)
    elif exceedings_ndn_8h_young(hand) is not None and exceedings_ndn_05h_young(hand) is not None:
        result = max(exceedings_ndn_8h_young(hand), exceedings_ndn_05h_young(hand))

    return result


def multiplicity_young(hand: str):                                                                       #H22
    result = None

    if num_values_exceeded_young(hand=hand) is not None:
        result = round(num_values_exceeded_young(hand=hand), MULTIPLICITIES_ROUN_UP_TO)

    return result


def s(activity: Activity, axis: str,):                                                                  #O20
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


def uprobkj(activity: Activity, axis: str,):                                                                 #O21
    if activity.measurement_time is not None:

        if activity.measurements.count() > 1:
            if axis.lower() == "x":
                uprobkj = activity.s_axis_x / ((activity.measurements.count() ** 0.5) * activity.ahwx)
            elif axis.lower() == "y":
                uprobkj = activity.s_axis_y / ((activity.measurements.count() ** 0.5) * activity.ahwy)
            elif axis.lower() == "z":
                uprobkj = activity.s_axis_z / ((activity.measurements.count() ** 0.5) * activity.ahwz)
            return round(uprobkj, 5)

        if activity.measurements.count() == 1:
            return 0

    return None


def ucj(activity: Activity, axis: str,):                                                                         #O22
    ucj = None

    if activity.measurement_time is not None:
        if axis.lower() == "x":
            ucj = (activity.uprobkj_x ** 2 + (COMBINED_STANDARD_UNCERTAINTY /100) ** 2) ** 0.5
        elif axis.lower() == "y":
            ucj = (activity.uprobkj_y ** 2 + (COMBINED_STANDARD_UNCERTAINTY /100) ** 2) ** 0.5
        elif axis.lower() == "z":
            ucj = (activity.uprobkj_z ** 2 + (COMBINED_STANDARD_UNCERTAINTY /100) ** 2) ** 0.5

        return round(ucj, 5)

    return ucj


def uhvi(activity: Activity):                                                              #BG11 = #R22
    if activity.measurements is not None:
        if activity.vector_summ > 0:
            activity.uhvi = round((((((activity.ucj_x * (activity.ahwx ** 2)) ** 2) +
                             ((activity.ucj_y * (activity.ahwy ** 2)) ** 2) +
                              ((activity.ucj_z * (activity.ahwz ** 2)) ** 2))) / activity.vector_summ ** 2)
                                  ** 0.5, 5)

            return activity.uhvi

    return None


def cai(activity: Activity):                                                                          #BI11
    if activity.measurement_time is not None and value_a8("right") is not None:                        #??? right(should be activity.hand)
        if value_a8("right") > 0:
            cai = activity.measurement_time * activity.vector_summ / (480 * value_a8("right"))
            return cai

    return None





def caiuci2(activity: Activity):                                                                        #BJ11-16
    if activity.measurement_time is not None:
        return (activity.uhvi * activity.cai) ** 2

    return None



#
# def uti_rh():                                     +++                                                          #BB11 - BB16
#     =ЕСЛИ(BA11="";
#     "";
#     ЕСЛИ(СЧЁТ(Q1: Q3)=1;
#     0;
#     ЕСЛИ(СЧЁТ(Q1: Q3)=2;
#     ОКРУГЛ((МАКС(Q1:Q3) - МИН(Q1: Q3)) / 2;
#     2);ОКРУГЛ(СТОТКЛ(Q1: Q3) / КОРЕНЬ(3);
#     2))))





# def uti_lh():                                       +++                                                         # BB11 - BB16
#     =ЕСЛИ(BA11="";
#     "";
#     ЕСЛИ(СЧЁТ(Q1: Q3)=1;
#     0;
#     ЕСЛИ(СЧЁТ(Q1: Q3)=2;
#     ОКРУГЛ((МАКС(Q1:Q3) - МИН(Q1: Q3)) / 2;
#     2);ОКРУГЛ(СТОТКЛ(Q1: Q3) / КОРЕНЬ(3);
#     2))))


#
# def cti__lh_rh():                                            +++                             #BK11 -BK16   BK36 - BK41
#     =ЕСЛИ(BA11="";
#     "";
#     BF11 ^ 2 / (2 * 480 *$BG$20))




# def ctiuti2():                                            +++                                                  #BL11 -BL16
#     =ЕСЛИ(BA11="";
#     "";
#     (BB11 * BK11) ^ 2)
# #

# def caiuci2__lh_rh():                                      +++                                        #BJ11-BJ16 BJ36 - BJ41
#     =ЕСЛИ(BA11="";
#     "";
#     (BG11 * BI11) ^ 2)




# #
# def uca8(hand: str):                                         +++                                           #BG21
#
#     =ЕСЛИ(Q1="";
#     "";
#     КОРЕНЬ(СУММ(BJ11: BJ16;
#     BL11: BL16)))



# def _2xuca8(hand: str):                                       +++                                            #BG22
#     if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
#         return 2 * BG21
#     return None



# def daily_exposure(hand: str):                          +++                                                  #H17
#     result = None
#
#     if Activity.objects.filter(measurements__isnull=False, hand=hand).exists():
#
#         if hand_exposure_time(hand=hand) is not None and hand_exposure_time(hand=hand) > 30:
#             first_value = round(value_a8(hand=hand), RES_ROUND_UP_TO)
#             second_value = round(, RES_ROUND_UP_TO)
#
#             result = f"{first_value} symbol {second_value}"
#
#         is sum>30:
#             res
#         else:
#             return "NOOO"
#
#     return None
#
#
# =ЕСЛИ(A11="";"";ЕСЛИ(СУММ(D11:D16)>30;СЦЕПИТЬ(ФИКСИРОВАННЫЙ(BG20;L3);СИМВОЛ(177);ФИКСИРОВАННЫЙ(BG22;L3));
# СЦЕПИТЬ("Nie dotyczy (";ФИКСИРОВАННЫЙ(BG20;L3);СИМВОЛ(177);ФИКСИРОВАННЫЙ(BG22;L3);")")))

#
# def ahvmax():                                         +++                                                      BG17
#
# =ЕСЛИ(BA11="";
# "";
# ЕСЛИ(BM9 < 1;
# "Nie dotyczy";
# МАКС(BM11: BM16)))



#
#
#
# def uahv():                                                                                          #BN11 - BN16
#     =ЕСЛИ(BM12="";
#     "";
#     BG12)
#
#
#
#
#
# def ucahvmax():                                                                                        #BG18
#     =ЕСЛИ(BG17="";
#     "";
#     ЕСЛИ(BM9 < 1;
#     "Nie dotyczy";
#     ЕСЛИ(BG17=BM11;
#     BN11;
#     ЕСЛИ(BG17=BM12;
#     BN12;
#     ЕСЛИ(BG17=BM13;
#     BN13;
#     ЕСЛИ(BG17=BM14;
#     BN14;
#     ЕСЛИ(BG17=BM15;
#     BN15;
#     ЕСЛИ(BG17=BM16;
#     BN16;
#     ""))))))))
#
#
#
#
#
# def xucahvmax2():                                                                                              #BG19
# =ЕСЛИ(BA11="";"";ЕСЛИ(BM9<1;"Nie dotyczy";2*BG18))
#
#
#
#
# # def H18():                                                                                              #H18
# #     =ЕСЛИ(A11="";
# #     "";
# #     ЕСЛИ(BM9 < 1;
# #     "Nie dotyczy";
# #     СЦЕПИТЬ(ФИКСИРОВАННЫЙ(BG17;
# #     L3);СИМВОЛ(177);
#     ФИКСИРОВАННЫЙ(BG19;
#     L3))))
#

