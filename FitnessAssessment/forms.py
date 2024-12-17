from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]


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
        fields = ["customer", "weight_in_kg", "bone_mass"]
