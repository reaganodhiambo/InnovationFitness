from django import forms
from .models import *


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class OneMileTestForm(forms.ModelForm):
    class Meta:
        model = TestInput
        fields = ["customer", "weight_in_kg", "one_mile_time", "exercise_heart_rate"]


class TestInputForm(forms.ModelForm):
    class Meta:
        model = TestInput
        fields = "__all__"


class ChestPressForm(forms.ModelForm):
    performance = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Repetion Maximum (In Pounds)"
    )

    class Meta:
        model = PerformanceInput
        fields = "__all__"


class WaistHipRatioForm(forms.ModelForm):
    performance = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Waist Hip Ratio"
    )

    class Meta:
        model = PerformanceInput
        fields = "__all__"
