from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = "__all__"
        widgets = {"user": forms.HiddenInput()}


class TheOneMileTestForm(forms.ModelForm):

    class Meta:
        model = TheOneMileTest
        fields = "__all__"
        widgets = {
            "oxygen_consumption": forms.HiddenInput(),
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
            "test_date": forms.DateInput(attrs={"readonly": "readonly"}),
        }


class MaximumChestPressTestForm(forms.ModelForm):

    class Meta:
        model = MaximumChestPressTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class SixtySecondSitUpTestForm(forms.ModelForm):

    class Meta:
        model = SixtySecondSitUpTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class ThePushUpTestForm(forms.ModelForm):

    class Meta:
        model = ThePushUpTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class SitAndReachTestForm(forms.ModelForm):

    class Meta:
        model = SitAndReachTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class WaistHipRatioTestForm(forms.ModelForm):

    class Meta:
        model = WaistHipRatioTest
        fields = "__all__"
        widgets = {
            "waist_hip_ratio": forms.HiddenInput(),
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class BMITestForm(forms.ModelForm):

    class Meta:
        model = BMITest
        fields = "__all__"
        widgets = {
            "bmi": forms.HiddenInput(),
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class BodyFatTestForm(forms.ModelForm):

    class Meta:
        model = BodyFatTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class VisceralFatRatingTestForm(forms.ModelForm):

    class Meta:
        model = VisceralFatRatingTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }


class MuscleMassTestForm(forms.ModelForm):

    class Meta:
        model = MuscleMassTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }

class BoneMassTestForm(forms.ModelForm):

    class Meta:
        model = BoneMassTest
        fields = "__all__"
        widgets = {
            "rating": forms.HiddenInput(),
            "score": forms.HiddenInput(),
            "customer": forms.HiddenInput(),
        }