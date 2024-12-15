from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from .utils import calculate_one_mile_test, calculate_max_chest_press
from django.db import connection
from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Max, Q
import datetime


# Create your views here.
def index(request):
    test_urls = {
        "The One Mile Test": "onemiletest",
        "Maximum Chest Press Test": "chest_press",
        "The 60 Second Sit-up Test": "situps",
        "The Push-up Test": "pushups",
        "Sit-and-Reach Test": "sitandreach",
        "Waist Hip Ratio": "waisthipratio",
        "Body Mass Index": "bmi",
        "Body Fat": "bodyfat",
        "Visceral Fat Rating": "visceral_fat",
        "Bone Mass": "bonemass",
    }

    # tests = FitnessTest.objects.all()
    # context = {"tests": tests}
    context = {"test_urls": test_urls}
    return render(request, "home.html", context=context)


def registerCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data.get("id")
            form.save()
            HttpResponse("Customer Registered")
            return redirect("onemiletest")

        else:
            return HttpResponse("Invalid Form")
    else:
        form = CustomerForm()
    context = {"form": form}
    return render(request, "register_customer.html", context=context)


"""One Mile Test"""


def oneMileTest(request):
    test_model = OneMileTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = OneMileTestForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            weight = form.cleaned_data["weight_in_kg"]
            exercise_heart_rate = form.cleaned_data["exercise_heart_rate"]
            one_mile_time = form.cleaned_data["one_mile_time"]

            performance = calculate_one_mile_test(
                weight=weight,
                age=customer.age,
                gender=customer.gender,
                time=one_mile_time,
                heart_rate=exercise_heart_rate,
            )

            scoring = age_gender_performance_rating(
                gender=customer.gender,
                age=customer.age,
                performance=performance,
                test_model=OneMileTestPerformance,
            )
            print("performance: ", performance)
            print(scoring)

            test_input_instance = get_test_input_instance(
                customer.id, datetime.date.today()
            )

            test_input_instance.weight_in_kg = weight
            test_input_instance.one_mile_time = one_mile_time
            test_input_instance.exercise_heart_rate = exercise_heart_rate

            test_input_instance.save(
                update_fields=["weight_in_kg", "one_mile_time", "exercise_heart_rate"]
            )

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return redirect("home")

    else:
        form = OneMileTestForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


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

    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result


"""Max Chest Press"""


def chestPress(request):

    test_model = MaximumChestPressPerformance.objects.all()[0]
    print("MaximumChestPressPerformance name: ", test_model.test_name)

    if request.method == "POST":
        form = ChestPressForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            weight = form.cleaned_data["weight_in_kg"]
            repetition_maximum = form.cleaned_data["weight_in_kg"]

            performance = calculate_max_chest_press(weight, repetition_maximum)
            print("Performance: ", performance)

            scoring = age_gender_performance_rating(
                gender=customer.gender,
                age=customer.age,
                performance=performance,
                test_model=MaximumChestPressPerformance,
            )
            print("Scoring: ", scoring)

            test_input_instance = get_test_input_instance(
                customer.id, datetime.date.today()
            )
            test_input_instance.weight_in_kg = weight
            test_input_instance.repetition_maximum = repetition_maximum

            test_input_instance.save(
                update_fields=["weight_in_kg", "repetition_maximum"]
            )

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = ChestPressForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""60 Sec sit up test"""


def situpTest(request):
    test_model = SixtySecSitUpTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = SitupForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            no_of_situps = form.cleaned_data["no_of_situps"]

            performance = no_of_situps
            print("Performance: ", performance)

            scoring = age_gender_performance_rating(
                gender=customer.gender,
                age=customer.age,
                performance=performance,
                test_model=SixtySecSitUpTestPerformance,
            )
            print("Scoring: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.no_of_situps = no_of_situps

            test_input_instance.save(update_fields=["no_of_situps"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = SitupForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Push Up test"""


def pushupTest(request):
    test_model = ThePushUpTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = PushupForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            no_of_push_ups = form.cleaned_data["no_of_push_ups"]

            performance = no_of_push_ups
            print("Performance: ", performance)

            scoring = age_gender_performance_rating(
                gender=customer.gender,
                age=customer.age,
                performance=performance,
                test_model=ThePushUpTestPerformance,
            )
            print("Scoring: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.no_of_push_ups = no_of_push_ups

            test_input_instance.save(update_fields=["no_of_push_ups"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = PushupForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""sit and reach test"""


def sitAndReachTest(request):
    test_model = SitAndReachTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = SitAndReachForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            sit_and_reach = form.cleaned_data["sit_and_reach"]

            performance = sit_and_reach
            print("Performance: ", performance)

            scoring = age_gender_performance_rating(
                gender=customer.gender,
                age=customer.age,
                performance=performance,
                test_model=SitAndReachTestPerformance,
            )
            print("Scoring: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.sit_and_reach = sit_and_reach

            test_input_instance.save(update_fields=["sit_and_reach"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = SitAndReachForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Waist Hip ratio"""


def waistHipRatioTest(request):
    test_model = WaistHipRatioTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = WaistHipRatioForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            hip_measurement = form.cleaned_data["hip_measurement"]
            waist_measurement = form.cleaned_data["waist_measurement"]

            performance = waist_measurement / hip_measurement

            scoring = age_gender_performance_rating(
                test_model=WaistHipRatioTestPerformance,
                gender=customer.gender,
                age=customer.age,
                performance=performance,
            )
            print("scoring waisthip: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.hip_measurement = hip_measurement
            test_input_instance.waist_measurement = waist_measurement

            test_input_instance.save(
                update_fields=["hip_measurement", "waist_measurement"]
            )

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = WaistHipRatioForm()
    context = {"form": form, "test_name": test_model.test_name}

    return render(request, "test_input.html", context=context)


"""Body Mass Index(BMI)"""


def bmiTest(request):
    test_model = BMITestPerformance.objects.all()[0]
    if request.method == "POST":
        form = BMIForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            height_in_cm = form.cleaned_data["height_in_cm"]
            weight_in_kg = form.cleaned_data["weight_in_kg"]

            BMI = weight_in_kg / (height_in_cm / 100) ** 2

            scoring = limit_type_performance_rating(
                test_model=BMITestPerformance,
                performance=BMI,
            )
            print("scoring BMI: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.height_in_cm = height_in_cm
            test_input_instance.weight_in_kg = weight_in_kg

            test_input_instance.save(update_fields=["height_in_cm", "weight_in_kg"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return redirect("home")
    else:
        form = BMIForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


def visceralFatTest(request):
    test_model = VisceralFatRatingTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = VisceralFatForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            visceral_fat_rating = form.cleaned_data["visceral_fat_rating"]

            scoring = limit_type_performance_rating(
                test_model=VisceralFatRatingTestPerformance,
                performance=visceral_fat_rating,
            )
            print("scoring BMI: ", scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )
            test_input_instance.visceral_fat_rating = visceral_fat_rating

            test_input_instance.save(update_fields=["visceral_fat_rating"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return redirect("home")
    else:
        form = VisceralFatForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Body Fat"""


def bodyFatTest(request):
    test_model = BodyFatTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = BodyFatForm(request.POST)

        if form.is_valid():
            customer = form.cleaned_data["customer"]
            percentage_body_fat = form.cleaned_data["percentage_body_fat"]

            performance = percentage_body_fat

            scoring = age_gender_performance_rating(
                test_model=BodyFatTestPerformance,
                gender=customer.gender,
                age=customer.age,
                performance=performance,
            )

            test_input_instance = get_test_input_instance(
                customer,
                datetime.date.today(),
            )
            test_input_instance.percentage_body_fat = percentage_body_fat

            test_input_instance.save(update_fields=["percentage_body_fat"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")
    else:
        form = BodyFatForm()
    context = {"form": form, "test_name": test_model.test_name}

    return render(request, "test_input.html", context=context)


def boneMassTest(request):
    test_model = BoneMassTestPerformance2.objects.all()[0]
    if request.method == "POST":
        form = BoneMassForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            bone_mass = form.cleaned_data["bone_mass"]
            weight = form.cleaned_data["weight"]

            scoring = performance_rating_lookup(
                gender=customer.gender,
                weight=weight,
                test_model=BoneMassTestPerformance2,
                performance=bone_mass,
            )

            test_input_instance = get_test_input_instance(
                customer.id, datetime.date.today()
            )
            test_input_instance.bone_mass = bone_mass

            test_input_instance.save(update_fields=["bone_mass"])

            record_test_score(
                customer=customer,
                test_name=test_model.test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return redirect("home")
    else:
        form = BoneMassForm()
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


def record_test_score(customer, test_name, rating, score, test_date):
    print("test_date: ", test_date)
    test_performances = TestPerformance.objects.filter(
        customer=customer, test_name=test_name, test_date=test_date
    )
    if len(test_performances) < 1:
        test_record = TestPerformance.objects.create(
            customer=customer,
            test_name=test_name,
            test_date=test_date,
        )
    elif len(test_performances) > 1:
        return HttpResponse("Multiple test records returned")
    else:
        test_record = test_performances[0]

    test_record.rating = rating
    test_record.score = score
    test_record.save(update_fields=["rating", "score"])


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
    p = (
        test_model.objects.select_related(
            "test_name", "performance_limit_type", "rating"
        )
        .filter(
            weight_limit__gender__gender=gender,
            weight_limit=Case(
                When(
                    Q(weight_limit__limit_type__iexact="above")
                    & Q(weight_limit__lte=weight),
                    then=Value("above"),
                ),
                When(
                    Q(weight_limit__limit_type__iexact="from")
                    & Q(weight_limit__lte=weight),
                    then=Value("from"),
                ),
                When(
                    Q(weight_limit__limit_type__iexact="below")
                    & Q(pweight_limit__gt=weight),
                    then=Value("below"),
                ),
                default=Value("Not Found"),
                output_field=CharField(max_length=5),
            ),
            performance_limit_type__type=Case(
                When(
                    Q(performance_limit_type__type__iexact="above")
                    & Q(performance__lte=performance),
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
        .order_by("-performance")
        .first()
    )
    print("**********printing bone mass rating p*********  ", p)
    score = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__iexact=p.test_name
    ).first()

    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result
