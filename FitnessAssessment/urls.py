from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("register", registerCustomer, name="register_customer"),
    path("omt", oneMileTest, name="onemiletest"),
    path("chest_press", chestPress,name="chest_press"),
    path("waist_hip", waistHipRatio),
    path("update_performance", updatePerformance),
]
