from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="home"),
    path("register", registerUser, name="register"),
    path("login", loginUser, name="login"),
    path("logout/", logoutUser, name="logout"),
    path(
        "update_user_profile/<int:id>",
        updateUserProfile,
        name="update_user_profile",
    ),
    path("one-mile-test", TheOneMileTestView, name="one-mile-test"),
    path("chest-press-test", MaximumChestPressTestView, name="chest-press-test"),
    path("sit-up-test", SixtySecondSitUpTestView, name="sit-up-test"),
    path("push-up-test", ThePushUpTestView, name="push-up-test"),
    path("sit-and-reach-test", SitAndReachTestView, name="sit-and-reach-test"),
    path("waist-hip-ratio-test", WaistHipRatioTestView, name="waist-hip-ratio-test"),
    path("bmi", BMITestView, name="bmi-test"),
    path("visceral-fat-test", VisceralFatTestView, name="visceral-fat-test"),
    path("bone-mass-test", BoneMassTestView, name="bone-mass-test"),
    path("body-fat-test", BodyFatTestView, name="body-fat-test"),
    path("latest-results", latestTestResultsView, name="latest-results"),
    path("fitness-tests", testGuideView, name="fitness-tests"),
    path("edit-profile/<int:id>", editUserProfile, name="edit_user_profile"),
    path("final-score", finalScoreView, name="final-score"),
]
