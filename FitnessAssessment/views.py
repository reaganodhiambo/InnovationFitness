from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from .utils import *
from django.db import connection
from django.db.models import Case, When, PositiveIntegerField, CharField, Value, Max, Q
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from typing import Final
from CustomerFitness.models import UserTestProfile

# Create your views here.


@login_required(login_url="login")
def index(request):
    user = request.user
    try:
        admin = user.is_staff
        user_profile = UserProfile.objects.get(user=user.id)
    except:
        return redirect("update_user_profile", user.id)

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

    context = {"test_urls": test_urls, "user": user}
    return render(request, "home.html", context=context)


def registerUser(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context=context)


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm()
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserTestProfile.objects.get(user_id=user.id)
            except:
                user_profile = None

            if not user_profile:
                return redirect("update-profile", user.id)
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, "login.html", context=context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def updateUserProfile(request, id):
    user = User.objects.get(id=id)

    if request.user.id == user.id:
        try:
            user_profile = UserProfile.objects.get(user_id=id)
            initial = user_profile
        except:
            user_profile = None

        initial = user_profile
        if request.method == "POST":
            form = UserProfileForm(
                request.POST,
                instance=initial,
            )

            if form.is_valid():
                updated_form = form.save(commit=False)
                updated_form.user_id = user.id
                print("updated_form: ", updated_form)
                updated_form.save()
                return redirect("home")
        else:
            form = UserProfileForm(instance=initial)
    else:
        messages.error(request, "You are not authorized to update this user's profile")
        return redirect(request.path_info)

    context = {"form": form, "user": user, "user_profile": user_profile}
    return render(request, "update_user_profile.html", context=context)


"""One Mile Test"""


@login_required(login_url="login")
def oneMileTest(request):
    test_model = OneMileTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = OneMileTestForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)

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
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "weight_in_kg": None,
            "one_mile_time": None,
            "exercise_heart_rate": None,
        }
        form = OneMileTestForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)



"""Max Chest Press"""


@login_required(login_url="login")
def chestPress(request):
    test_model = MaximumChestPressPerformance.objects.all()[0]
    if request.method == "POST":
        form = ChestPressForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)

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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "weight_in_kg": None,
            "repetition_maximum": None,
        }
        form = ChestPressForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""60 Sec sit up test"""


@login_required(login_url="login")
def situpTest(request):
    test_model = SixtySecSitUpTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = SitupForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "no_of_situps": None,
        }
        form = SitupForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Push Up test"""


@login_required(login_url="login")
def pushupTest(request):
    test_model = ThePushUpTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = PushupForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "no_of_push_ups": None,
        }
        form = PushupForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""sit and reach test"""


@login_required(login_url="login")
def sitAndReachTest(request):
    test_model = SitAndReachTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = SitAndReachForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
            customer = form.cleaned_data["customer"]
            sit_and_reach = form.cleaned_data["sit_and_reach"]

            performance = sit_and_reach

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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "sit_and_reach": None,
        }
        form = SitAndReachForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Waist Hip ratio"""


@login_required(login_url="login")
def waistHipRatioTest(request):
    test_model = WaistHipRatioTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = WaistHipRatioForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "hip_measurement": None,
            "waist_measurement": None,
        }
        form = WaistHipRatioForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}

    return render(request, "test_input.html", context=context)


"""Body Mass Index(BMI)"""


@login_required(login_url="login")
def bmiTest(request):
    test_model = BMITestPerformance.objects.all()[0]
    if request.method == "POST":
        form = BMIForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "height_in_cm": None,
            "weight_in_kg": None,
        }
        form = BMIForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def visceralFatTest(request):
    test_model = VisceralFatRatingTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = VisceralFatForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "visceral_fat_rating": None,
        }
        form = VisceralFatForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""Body Fat"""


@login_required(login_url="login")
def bodyFatTest(request):
    test_model = BodyFatTestPerformance.objects.all()[0]
    if request.method == "POST":
        form = BodyFatForm(request.POST)

        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
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
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "percentage_body_fat": None,
        }
        form = BodyFatForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}

    return render(request, "test_input.html", context=context)


"""Bone Mass"""


@login_required(login_url="login")
def boneMassTest(request):
    # test_model = WeightGenderPerformanceRating.objects.all()[0]
    test_model = FitnessTest.objects.get(test_name="Bone Mass")

    if request.method == "POST":
        form = BoneMassForm(request.POST)
        if form.is_valid():
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(
                    request,
                    "You are not authorized to update this customer's  test data",
                )
                return redirect(request.path_info)
            if request.user.id != form.cleaned_data["customer"].user.id:
                messages.error(request, "You are not authorized to update this customer's  test data")
                return redirect(request.path_info)

            customer = form.cleaned_data["customer"]
            bone_mass = form.cleaned_data["bone_mass"]
            weight = form.cleaned_data["weight_in_kg"]

            scoring = gender_weight_scoring(
                test_name=test_model.test_name,
                gender=customer.gender,
                weight=weight,
                scoring_model=WeightGenderPerformanceRating,
                performance=bone_mass,
            )
            print("scoring: ", scoring)
            test_input_instance = get_test_input_instance(
                customer.id, datetime.date.today()
            )
            test_input_instance.bone_mass = bone_mass
            test_input_instance.weight_in_kg = weight

            test_input_instance.save(update_fields=["bone_mass", "weight_in_kg"])

            record_test_score(
                customer=customer,
                test=test_model.id,
                rating=scoring["rating"],
                score=scoring["score"],
                test_date=datetime.date.today(),
            )
            return redirect("home")
    else:
        user_profile = UserProfile.objects.get(user=request.user.id)
        initial_dict = {
            "customer": user_profile,
            "bone_mass": None,
            "weight_in_kg": None,
        }
        form = BoneMassForm(initial=initial_dict)
    context = {"form": form, "test_name": test_model.test_name}
    return render(request, "test_input.html", context=context)


"""retrieve test performance  for a given customer and date"""


@login_required(login_url="login")
def get_test_performance(request):
    user = request.user
    customer = UserProfile.objects.get(user=user.id)
    if user:
        test_perf = TestPerformance.objects.filter(customer=customer).all()

    context = {"user": user, "test_perf": test_perf}
    return render(request, "test_performance.html", context=context)


