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


class ChestPressForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "weight_in_kg", "repetition_maximum"]


class SitupForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "no_of_situps"]


class PushupForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "no_of_push_ups"]


class SitAndReachForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "sit_and_reach"]


class WaistHipRatioForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "waist_measurement", "hip_measurement"]


class BMIForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "height_in_cm", "weight_in_kg"]


class VisceralFatForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "visceral_fat_rating"]


class BodyFatForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "percentage_body_fat"]


class BoneMassForm(forms.ModelForm):

    class Meta:
        model = TestInput
        fields = ["customer", "weight", "bone_mass"]
