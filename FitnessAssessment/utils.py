from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Max, Q
import datetime

# remove TestInput in future
from .models import TestInput, TestPerformance, PerformanceRatingScoring


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
    max_chest_press = (repetition_maximum * 2.205) / weight_in_pounds
    return max_chest_press



def record_test_score(customer, test, rating, score, test_date):
    print("test_date: ", test_date)
    test_performances = TestPerformance.objects.filter(
        customer=customer, test=test, test_date=test_date
    )
    if len(test_performances) < 1:
        test_record = TestPerformance.objects.create(
            customer=customer,
            test=test,
            test_date=test_date,
        )
    elif len(test_performances) > 1:
        return HttpResponse("Multiple test records returned")
    else:
        test_record = test_performances[0]

    test_record.rating = rating
    test_record.score = score
    test_record.save(update_fields=["rating", "score"])


# delete in future
def get_test_input_instance(customer_id, test_date):
    test_inputs = TestInput.objects.filter(customer_id=customer_id, test_date=test_date)

    if len(test_inputs) < 1:
        # create instance and save
        test_input_instance = TestInput.objects.create(
            customer_id=customer_id, test_date=test_date
        )
    elif len(test_inputs) > 1:
        # error - multiple items
        raise Exception("Multiple test input records returned")
    else:
        test_input_instance = test_inputs[0]

    return test_input_instance


def limit_type_performance_rating(performance, test_model):
    p = (
        test_model.objects.select_related("test_name", "limit_type", "rating")
        .filter(
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
    print("**********printing one mile test rating p*********  ", p)
    score = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__iexact=p.test_name
    ).first()

    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result


def performance_rating_lookup(gender, weight, performance, test_model):
    print("gender, weight, performance: ", gender, weight, performance)
    p = (
        test_model.objects.select_related(
            "test_name", "performance_limit_type", "rating"
        )
        .filter(
            weight_limit__gender__gender=gender,
            weight_limit__limit_type__type=Case(
                When(
                    Q(weight_limit__limit_type__type__iexact="above")
                    & Q(weight_limit__weight_limit__lt=weight),
                    then=Value("above"),
                ),
                When(
                    Q(weight_limit__limit_type__type__iexact="from")
                    & Q(weight_limit__weight_limit__lte=weight),
                    then=Value("from"),
                ),
                When(
                    Q(weight_limit__limit_type__type__iexact="below")
                    & Q(weight_limit__weight_limit__gt=weight),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
            performance_limit_type__type=Case(
                When(
                    Q(performance_limit_type__type__iexact="above")
                    & Q(performance__lt=performance),
                    then=Value("above"),
                ),
                When(
                    Q(performance_limit_type__type__iexact="from")
                    & Q(performance__lte=performance),
                    then=Value("from"),
                ),
                When(
                    Q(performance_limit_type__type__iexact="below")
                    & Q(performance__gt=performance),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-weight_limit", "-performance")
        .first()
    )

    score = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__iexact=p.test_name
    ).first()

    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result


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


# print(gender_age_scoring("male", 34, 38.9, AgeGenderPerformanceRating))
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


def age_gender_performance_rating(gender, age, performance, test_model):
    p = (
        test_model.objects.select_related("test_name", "gender", "limit_type", "rating")
        .filter(
            gender__gender=gender,
            min_age__lte=Case(
                When(min_age__isnull=True, then=age),
                default="min_age",
                output_field=PositiveIntegerField(),
            ),
            max_age__gte=Case(
                When(max_age__isnull=True, then=age),
                default="max_age",
                output_field=PositiveIntegerField(),
            ),
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
    print("**********printing one mile test rating p*********  ", p)
    score = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__iexact=p.test_name
    ).first()
    print("score", score)
    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result
