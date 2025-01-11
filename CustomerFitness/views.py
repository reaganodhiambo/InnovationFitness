from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from FitnessAssessment.models import AgeGenderPerformanceRating,FitnessTest
from FitnessAssessment.utils import *


@login_required(login_url="login")
def updateUserProfile(request, id):
    user = User.objects.get(id=id)
    print("user: ", user.id)
    print("request.user: ", request.user.id)

    if request.user.id == user.id:
        try:
            user_profile = UserTestProfile.objects.get(user_id=id)
        except:
            user_profile = None

        if request.method == "POST":
            form = UserTestProfileForm(
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
            if user_profile is not None:
                form = UserTestProfileForm(instance=user_profile)
            else:
                initial_dict = {"user": user}
                form = UserTestProfileForm(initial=initial_dict)
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
        user_profile = UserTestProfile.objects.get(user_id=user.id)
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

            performance = calculate_one_mile_test(
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
                performance=performance,
                scoring_model=AgeGenderPerformanceRating,
            )
            print("scoring: ", score)

            form.save()

            test_model = FitnessTest.objects.get(test_name=test_name)
            record_test_score(
                customer=user_profile.id,
                test=test_model.id,
                rating=score["rating"],
                score=score["score"],
                test_date=datetime.date.today(),
            )

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
        user_profile = UserTestProfile.objects.get(user=user)
    except:
        user_profile = None

    if request.method == "POST":
        form = MaximumChestPressTestForm(
            request.POST,
        )
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.customer = user_profile
            updated_form.save()
            return redirect("home")
        else:
            return HttpResponse("Form is not valid")
    else:
        form = MaximumChestPressTestForm(instance=user_profile)

    context = {
        "form": form,
        "user": user,
        "user_profile": user_profile,
        "test_name": test_name,
    }
    return render(request, "test_input.html", context=context)
