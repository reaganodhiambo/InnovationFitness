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
        "The One Mile Test": "one-mile-test",
        "Maximum Chest Press Test": "chest-press-test",
        "The 60 Second Sit-up Test": "sit-up-test",
        "The Push-up Test": "push-up-test",
        "Sit-and-Reach Test": "sit-and-reach-test",
        "Waist Hip Ratio": "waist-hip-ratio-test",
        "Body Mass Index": "bmi-test",
        "Body Fat": "body-fat-test",
        "Visceral Fat Rating": "visceral-fat-test",
        "Bone Mass": "bone-mass-test",
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
                user_profile = UserProfile.objects.get(user_id=user.id)
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
    print("user: ", user.id)
    print("request.user: ", request.user.id)

    if request.user.id == user.id:
        try:
            user_profile = UserProfile.objects.get(user_id=id)
        except:
            user_profile = None
        print("user_profile: ", user_profile)
        if request.method == "POST":
            form = UserProfileForm(
                request.POST,
                instance=user_profile,
            )

            if form.is_valid():
                updated_form = form.save(commit=False)
                updated_form.user_id = user.id
                updated_form.save()
                return redirect("home")
            else:
                return HttpResponse("Form is not valid")
        else:
            print("user profile", user_profile)
            if user_profile is not None:
                form = UserProfileForm(instance=user_profile)
            else:
                initial_dict = {"user": user}
                form = UserProfileForm(initial=initial_dict)
    else:
        messages.error(request, "You are not authorized to update this user's profile")
        return redirect(request.path_info)

    context = {"form": form, "user": user, "user_profile": user_profile}
    return render(request, "update_user_profile.html", context=context)


@login_required(login_url="login")
def TheOneMileTestView(request):
    test_name = "The One Mile Test"
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user_id=user.id)
    except:
        user_profile = None

    if request.method == "POST":
        form = TheOneMileTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            weight = form.cleaned_data["weight"]
            one_mile_time = form.cleaned_data["one_mile_time"]
            exercise_heart_rate = form.cleaned_data["exercise_heart_rate"]

            oxygen_consumption = calculate_one_mile_test(
                weight=weight,
                age=age,
                gender=customer.gender,
                time=one_mile_time,
                heart_rate=exercise_heart_rate,
            )

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=oxygen_consumption,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.oxygen_consumption = oxygen_consumption
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
            "height": user_profile.height,
            "weight": user_profile.weight,
        }
        form = TheOneMileTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def MaximumChestPressTestView(request):
    test_name = "Maximum Chest Press Test"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = MaximumChestPressTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            weight = form.cleaned_data["weight"]
            repetition_maximum = form.cleaned_data["repetition_maximum"]

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=calculate_max_chest_press(weight, repetition_maximum),
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
            "height": user_profile.height,
            "weight": user_profile.weight,
        }
        form = MaximumChestPressTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def SixtySecondSitUpTestView(request):
    test_name = "The 60 Second Sit-up Test"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = SixtySecondSitUpTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            no_of_situps = form.cleaned_data["no_of_situps"]

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=no_of_situps,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
        }
        form = SixtySecondSitUpTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def ThePushUpTestView(request):
    test_name = "The Push-up Test"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = ThePushUpTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            no_of_push_ups = form.cleaned_data["no_of_push_ups"]

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=no_of_push_ups,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
        }
        form = ThePushUpTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def SitAndReachTestView(request):
    test_name = "Sit-and-Reach Test"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = SitAndReachTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            reach_in_cm = form.cleaned_data["reach_in_cm"]

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=reach_in_cm,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
        }
        form = SitAndReachTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def WaistHipRatioTestView(request):
    test_name = "Waist Hip Ratio"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = WaistHipRatioTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            waist_measurement = form.cleaned_data["waist_measurement"]
            hip_measurement = form.cleaned_data["hip_measurement"]

            waist_hip_ratio = waist_measurement / hip_measurement

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=waist_hip_ratio,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.waist_hip_ratio = waist_hip_ratio
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
        }
        form = WaistHipRatioTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def BMITestView(request):
    test_name = "Body Mass Index"
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = BMITestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            height = form.cleaned_data["height"]
            weight = form.cleaned_data["weight"]

            bmi = weight / (height / 100) ** 2
            print("bmi: ", bmi)
            score = limit_type_scoring(
                performance=bmi,
                test_model=BMITestPerformance,
            )
            print("score: ", score)
            initial_obj = form.save(commit=False)
            initial_obj.bmi = bmi
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]
            print("initial_obj: ", initial_obj)
            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
            "height": user_profile.height,
            "weight": user_profile.weight,
        }
        form = BMITestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


@login_required(login_url="login")
def VisceralFatTestView(request):
    test_name = "Visceral Fat Rating"
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = VisceralFatRatingTestForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            visceral_fat_rating = form.cleaned_data["visceral_fat_rating"]

            score = limit_type_scoring(
                performance=visceral_fat_rating,
                test_model=VisceralFatRatingTestPerformance,
            )
            print("score: ", score)
            initial_obj = form.save(commit=False)
            initial_obj.visceral_fat_rating = visceral_fat_rating
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]
            print("initial_obj: ", initial_obj)
            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
        }
        form = VisceralFatRatingTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


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


@login_required(login_url="login")
def BoneMassTestView(request):
    test_name = "Bone Mass"
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = BoneMassTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            weight = form.cleaned_data["weight"]
            bone_mass = form.cleaned_data["bone_mass"]

            score = gender_weight_scoring(
                test_name=test_name,
                gender=customer.gender,
                weight=weight,
                performance=bone_mass,
                scoring_model=WeightGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        # else:
        #     return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "weight": user_profile.weight,
        }
        form = BoneMassTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)


def BodyFatTestView(request):
    test_name = "Body Fat"
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user_id=user.id)
    except:
        user_profile = None

    if request.method == "POST":
        form = BodyFatTestForm(
            request.POST,
        )
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            age = form.cleaned_data["age"]
            body_fat_percentage = form.cleaned_data["body_fat_percentage"]

            score = gender_age_scoring(
                test_name=test_name,
                gender=customer.gender,
                age=age,
                performance=body_fat_percentage,
                scoring_model=AgeGenderPerformanceRating,
            )

            initial_obj = form.save(commit=False)
            initial_obj.body_fat_percentage = body_fat_percentage
            initial_obj.rating = score["rating"]
            initial_obj.score = score["score"]

            initial_obj.save()

            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        initial_dict = {
            "customer": user_profile,
            "age": user_profile.age,
        }
        form = BodyFatTestForm(initial=initial_dict)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)
