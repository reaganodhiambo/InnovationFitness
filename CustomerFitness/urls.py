from django.urls import path
from .views import *

urlpatterns = [
    path("update-profile/<int:id>", updateUserProfile, name="update-profile"),
    path("one-mile-test", TheOneMileTestView, name="one-mile-test"),
    path("chest-press-test", MaximumChestPressTestView, name="chest-press-test"),  
]
