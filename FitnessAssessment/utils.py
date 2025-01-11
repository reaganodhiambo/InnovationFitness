from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Q
from .models import (
    BMITestPerformance,
    PerformanceRatingScoring,
)


def calculate_one_mile_test(weight, age, gender, time, heart_rate):
    gender_value = 1 if gender.lower() == "male" else 0
    weight_in_pounds = weight * 2.205
    vo2_max = (
        132.853
        - (0.0769 * weight_in_pounds)
        - (0.3877 * age)
        + (6.315 * gender_value)
        - (3.2649 * float(time))
        - (0.1565 * float(heart_rate))
    )
    return vo2_max


def calculate_max_chest_press(weight, repetition_maximum):
    weight_in_pounds = weight * 2.205
    max_chest_press = (float(repetition_maximum) * 2.205) / weight_in_pounds
    return max_chest_press


def gender_age_scoring(test_name, gender, age, performance, scoring_model):

    ABOVE: Final(str) = "above"
    FROM: Final(str) = "from"
    BELOW: Final(str) = "below"

    p = (
        scoring_model.objects.filter(
            test__test_name=test_name,
            gender__gender=gender,
            age_limit_type__type=Case(
                When(
                    Q(age_limit_type__type__exact=ABOVE) & Q(age_limit__lt=age),
                    then=Value("above"),
                ),
                When(
                    Q(age_limit_type__type__exact=FROM) & Q(age_limit__lte=age),
                    then=Value("from"),
                ),
                When(
                    Q(age_limit_type__type__exact=BELOW) & Q(age_limit__gt=age),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
            performance_limit_type__type=Case(
                When(
                    Q(performance_limit_type__type__exact=ABOVE)
                    & Q(performance_limit__lt=performance),
                    then=Value("above"),
                ),
                When(
                    Q(performance_limit_type__type__exact=FROM)
                    & Q(performance_limit__lte=performance),
                    then=Value("from"),
                ),
                When(
                    Q(performance_limit_type__type__exact=BELOW)
                    & Q(performance_limit__gt=performance),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-age_limit", "-performance_limit")
        .first()
    )

    result = {
        "user_performance": performance,
        "performance_limit": p.performance_limit,
        "rating": p.rating.rating,
        "score": p.rating.score,
    }
    return result


def gender_weight_scoring(test_name, gender, weight, performance, scoring_model):

    ABOVE: Final(str) = "above"
    FROM: Final(str) = "from"
    BELOW: Final(str) = "below"

    p = (
        scoring_model.objects.filter(
            test__test_name=test_name,
            gender__gender=gender,
            weight_limit_type__type=Case(
                When(
                    Q(weight_limit_type__type__exact=ABOVE)
                    & Q(weight_limit__lt=weight),
                    then=Value("above"),
                ),
                When(
                    Q(weight_limit_type__type__exact=FROM)
                    & Q(weight_limit__lte=weight),
                    then=Value("from"),
                ),
                When(
                    Q(weight_limit_type__type__exact=BELOW)
                    & Q(weight_limit__gt=weight),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
            performance_limit_type__type=Case(
                When(
                    Q(performance_limit_type__type__exact=ABOVE)
                    & Q(performance_limit__lt=performance),
                    then=Value("above"),
                ),
                When(
                    Q(performance_limit_type__type__exact=FROM)
                    & Q(performance_limit__lte=performance),
                    then=Value("from"),
                ),
                When(
                    Q(performance_limit_type__type__exact=BELOW)
                    & Q(performance_limit__gt=performance),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-weight_limit", "-performance_limit")
        .first()
    )

    result = {
        "user_performance": performance,
        "performance_limit": p.performance_limit,
        "rating": p.rating.rating,
        "score": p.rating.score,
    }
    return result


def limit_type_scoring(performance, test_model):
    p = (
        test_model.objects.filter(
            limit_type__type=Case(
                When(
                    Q(limit_type__type__iexact="above")
                    & Q(performance__lte=performance),
                    then=Value("above"),
                ),
                When(
                    Q(limit_type__type__iexact="from")
                    & Q(performance__lte=performance),
                    then=Value("from"),
                ),
                When(
                    Q(limit_type__type__iexact="below")
                    & Q(performance__gt=performance),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-performance")
        .first()
    )

    result = {
        "performance": p.performance,
        "rating": p.rating.rating,
        "score": p.rating.score,
    }
    return result
