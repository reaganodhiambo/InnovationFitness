from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from .utils import calculate_one_mile_test
from django.db import connection
from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Max


# Create your views here.
def index(request):
    tests = FitnessTest.objects.all()
    context = {"tests":tests}
    return render(request, "home.html",context=context)


def registerCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data.get("id")
            form.save()
            HttpResponse("Customer Registered")
            return redirect("one_mile_test")

        else:
            return HttpResponse("Invalid Form")
    else:
        form = CustomerForm()
    context = {"form": form}
    return render(request, "register_customer.html", context=context)


def chestPress(request):
    test = FitnessTest.objects.filter(test_name__icontains="Maximum Chest Press Test")[
        0
    ]

    print(test.id, test.test_name, test.category)

    if request.method == "POST":
        form = ChestPressForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get("test_id").id != test.id:
                return HttpResponse("Corrupted input for test type")
            form.save()
            message = test.test_name + " Recorded"
            return HttpResponse(message)
        else:
            return HttpResponse("Invalid Form")
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


def oneMileTest(request):
    if request.method == "POST":
        # customer = Customer.objects.get(id=customer_id)
        form = OneMileTestForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            weight = form.cleaned_data["weight_in_kg"]
            exercise_heart_rate = form.cleaned_data["exercise_heart_rate"]
            one_mile_time = form.cleaned_data["one_mile_time"]

            new, created = TestInput.objects.update_or_create(
                customer=customer,
                defaults={
                    "weight_in_kg": weight,
                    "exercise_heart_rate": exercise_heart_rate,
                },
            )
            if created:
                return HttpResponse("Test Input Saved")
            else:
                return HttpResponse("Test Input Updated")
            # form.save()
            # return HttpResponse("One Mile Test Added")

    else:
        form = OneMileTestForm()
    context = {
        "form": form,
    }
    return render(request, "one_mile_test.html", context=context)


def testInput(request):
    if request.method == "POST":
        form = TestInputForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Test Input Added")
            return redirect("register_customer")
        else:
            return HttpResponse("Invalid form")
    else:
        form = TestInputForm()
    context = {
        "form": form,
    }

    # logic here
    # pick relevant fields for each test and use it to find scores
    return render(request, "testinput.html", context=context)


def calculate_results(request):
    input_data = TestInput.objects.all()
    for input_instance in input_data:
        age = input_instance.customer.age
        weight = input_instance.weight_in_kg
        gender = input_instance.customer.gender
        heart_rate = input_instance.exercise_heart_rate
        one_mile_time = input_instance.one_mile_time
        # one mile test
        one_mile = calculate_one_mile_test(
            weight=weight,
            age=age,
            gender=gender,
            time=one_mile_time,
            heart_rate=heart_rate,
        )
        gender_value = 1 if gender == "Male" else 0
        expected_performance = OneMileTestPerformance.objects.filter(
            min_age__lte=age,
            max_age__gte=age,
            gender__gender=gender,
        )

        for result in expected_performance:
            if result.limit_type.type == "from":
                print(result.performance)
            elif result.limit_type == "above":
                print(result.performance)
            else:
                print(result.limit_type.type)

        return HttpResponse(expected_performance)


def one_mile_test(request):
    p = (
        OneMileTestPerformance.objects.select_related(
            "test_name", "gender", "limit_type", "rating"
        )
        .filter(
            gender__gender="Male",
            min_age__lte=Case(
                When(min_age__isnull=True, then=60),
                default="min_age",
                output_field=PositiveIntegerField(),
            ),
            max_age__gte=Case(
                When(max_age__isnull=True, then=60),
                default="max_age",
                output_field=PositiveIntegerField(),
            ),
            limit_type__type=Case(
                When(performance__lt=33.5, then=Value("above")),
                When(performance__gt=33.5, then=Value("below")),
                default=Value("from"),
                output_field=CharField(max_length=5),
            ),
        )
        .order_by("-performance")
        .first()
    )
    y = PerformanceRatingScoring.objects.filter(
        rating__iexact=p.rating, test_name__test_name__icontains="mile"
    ).values_list("score", flat=True)
    print(y)
    return HttpResponse(y)
