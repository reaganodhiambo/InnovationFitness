from .models import *
from django import forms
from django.contrib.auth.models import User

class UserTestProfileForm(forms.ModelForm):

    class Meta:
        model = UserTestProfile
        fields = "__all__"
        widgets = {"user": forms.HiddenInput()}


class TheOneMileTestForm(forms.ModelForm):

    class Meta:
        model = TheOneMileTest
        fields = "__all__"
        # widgets = {"customer": forms.HiddenInput()}


class MaximumChestPressTestForm(forms.ModelForm):

    class Meta:
        model = MaximumChestPressTest
        fields = "__all__"
        # widgets = {"customer": forms.HiddenInput()}


class SixtySecondSitUpTestForm(forms.ModelForm):

    class Meta:
        model = SixtySecondSitUpTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class ThePushUpTestForm(forms.ModelForm):

    class Meta:
        model = ThePushUpTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class SitAndReachTestForm(forms.ModelForm):

    class Meta:
        model = SitAndReachTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class WaistHipRatioTestForm(forms.ModelForm):

    class Meta:
        model = WaistHipRatioTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class BMITestForm(forms.ModelForm):

    class Meta:
        model = BMITest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class BodyFatTestForm(forms.ModelForm):

    class Meta:
        model = BodyFatTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class VisceralFatRatingTestForm(forms.ModelForm):

    class Meta:
        model = VisceralFatRatingTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}


class MuscleMassTestForm(forms.ModelForm):

    class Meta:
        model = MuscleMassTest
        fields = "__all__"
        widgets = {"customer": forms.HiddenInput()}
