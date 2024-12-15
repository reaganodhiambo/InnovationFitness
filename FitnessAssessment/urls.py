from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("register", registerCustomer, name="register_customer"),
    path("omt", oneMileTest, name="onemiletest"),
    path("chest_press", chestPress, name="chest_press"),
    path("situps", situpTest, name="situps"),
    path("pushups", pushupTest, name="pushups"),
    path("sit-and-reach", sitAndReachTest, name="sitandreach"),
    path("waist-hip-ratio", waistHipRatioTest, name="waisthipratio"),
    path("bmi", bmiTest, name="bmi"),
    path("visceral_fat", visceralFatTest, name="visceral_fat"),
    path("body-fat", bodyFatTest, name="bodyfat"),
    path("bone-mass", boneMassTest, name="bonemass"),
]
