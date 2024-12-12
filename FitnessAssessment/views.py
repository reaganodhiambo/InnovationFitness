from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from .utils import calculate_one_mile_test
from django.db import connection
from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Max
import datetime


# Create your views here.
def index(request):
    tests = FitnessTest.objects.all()
    context = {"tests": tests}
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
    test_name = FitnessTest.objects.filter(test_name__icontains="mile")[0]
    if request.method == "POST":
        form = OneMileTestForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            weight = form.cleaned_data["weight_in_kg"]
            exercise_heart_rate = form.cleaned_data["exercise_heart_rate"]
            one_mile_time = form.cleaned_data["one_mile_time"]

            customer_instance = Customer.objects.get(id=customer.id)

            performance = calculate_one_mile_test(
                weight=weight,
                age=customer_instance.age,
                gender=customer_instance.gender,
                time=one_mile_time,
                heart_rate=exercise_heart_rate,
            )

            scoring = one_mile_test_rating(
                gender=customer_instance.gender,
                age=customer_instance.age,
                performance=performance,
            )
            print("performance: ", performance)
            print(scoring)

            test_input_instance = get_test_input_instance(
                customer, datetime.date.today()
            )

            test_input_instance.weight_in_kg = weight
            test_input_instance.one_mile_time = one_mile_time
            test_input_instance.exercise_heart_rate = exercise_heart_rate

            test_input_instance.save(
                update_fields=["weight_in_kg", "one_mile_time", "exercise_heart_rate"]
            )

            record_test_score(
                customer=customer,
                test_name=test_name,
                rating=scoring["rating"],
                score=scoring["user_score"],
                test_date=datetime.date.today(),
            )
            return HttpResponse("Form Saved Successfully")

    else:
        form = OneMileTestForm()
    context = {
        "form": form,
    }
    return render(request, "one_mile_test.html", context=context)


def one_mile_test_rating(gender, age, performance):
    print(gender, age, performance)
    p = (
        OneMileTestPerformance.objects.select_related(
            "test_name", "gender", "limit_type", "rating"
        )
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
                When(performance__lt=performance, then=Value("above")),
                When(performance__gt=performance, then=Value("below")),
                default=Value("from"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-performance")
        .first()
    )
    print("printitng p")
    print(p)
    score = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__icontains="mile"
    ).first()

    result = {
        "user_performance": p.performance,
        "user_score": score.score,
        "rating": score.rating,
    }
    return result


def chestPress(request):
    test = FitnessTest.objects.filter(test_name__icontains="Maximum Chest Press Test")[
        0
    ]

    print(test.id, test.test_name, test.category)

    weight = TestInput.objects.get(id=test.id)

    if request.method == "POST":
        form = ChestPressForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get("test_id").id != test.id:
                return HttpResponse("Corrupted input for test type")
            form.save()
            message = test.test_name + " Recorded"
            return HttpResponse(message)

    else:
        form = ChestPressForm(initial={"test_id": test})
    context = {
        "form": form,
        "test": test,
    }
    return render(request, "chest_press.html", context=context)


def waistHipRatio(request):
    test = FitnessTest.objects.filter(test_name__icontains="Hip")[0]

    print(test.id, test.test_name, test.category)

    if request.method == "POST":
        form = WaistHipRatioForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get("test_id").id != test.id:
                return HttpResponse("Corrupted input for test type")
            form.save()
            message = test.test_name + " Recorded"
            return HttpResponse(message)
        else:
            return HttpResponse("Invalid Form")
    else:
        form = WaistHipRatioForm(initial={"test_id": test})
    context = {
        "form": form,
        "test": test,
    }
    return render(request, "chest_press.html", context=context)


def updatePerformance(request):
    if request.method == "POST":
        test_id = FitnessTest.objects.get(
            test_name__icontains="Maximum Chest Press Test"
        )
        form = ChestPressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Chest Press Recorded")
        else:
            return HttpResponse("Invalid Form")
    else:
        form = ChestPressForm()
    context = {"form": form, "test_id": test_id}
    return render(request, "chest_press.html", context=context)


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
        # create instanc and save
        test_input_instance = TestInput.objects.create(
            customer_id=customer_id, test_date=test_date
        )
    elif len(test_inputs) > 1:
        # error - multiple items
        raise Exception("Multiple test input records returned")
    else:
        test_input_instance = test_inputs[0]

    return test_input_instance
