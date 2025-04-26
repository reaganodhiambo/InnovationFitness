from django.db import models
from django.db.models import When, Case, Value
from django.db.models.functions import Concat, Cast
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", blank=True
    )
    gender = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    gender = models.CharField(max_length=10, choices=gender)
    age = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True, verbose_name="Height (cm)")
    weight = models.PositiveIntegerField(null=True, verbose_name="Weight (kg)")
    phone_number = models.CharField(max_length=256, blank=False, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


class Category(models.Model):
    test_category = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.test_category


class FitnessTest(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=80, unique=True, blank=False)

    def __str__(self):
        return self.test_name

    class Meta:
        verbose_name = "Fitness Test"
        verbose_name_plural = "Fitness Tests"


class Gender(models.Model):
    gender_options = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(max_length=20, choices=gender_options)

    def __str__(self):
        return self.gender


class PerformanceRatingScoring(models.Model):
    ratings = (
        ("very poor", "very poor"),
        ("poor", "poor"),
        ("fair", "fair"),
        ("good", "good"),
        ("excellent", "excellent"),
        ("superior", "superior"),
        ("moderate", "moderate"),
        ("High", "High"),
        ("very high", "very high"),
        ("Very Low", "Very Low"),
        ("Low", "Low"),
        ("Slightly Low", "Slightly Low"),
        ("Desired", "Desired"),
        ("Slightly High", "Slightly High"),
        ("Very High", "Very High"),
        ("Healthy", "Healthy"),
        ("Low Risk", "Low Risk"),
        ("High Risk", "High Risk"),
        ("Very High Risk", "Very High Risk"),
        ("Desirable", "Desirable"),
        ("Underweight", "Underweight"),
        ("Overweight", "Overweight"),
        ("Obese", "Obese"),
        ("Extremely Obese", "Extremely Obese"),
    )
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    rating = models.CharField(max_length=30, choices=ratings)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("test_name", "rating")

    def __str__(self):
        return str(self.test_name) + ": " + str(self.rating)


class PerformanceLimit(models.Model):
    type = models.CharField(max_length=10)
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.type


class AgeGenderPerformanceRating(models.Model):
    test = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    age_limit_type = models.ForeignKey(
        PerformanceLimit, related_name="PerformanceLimit_1", on_delete=models.PROTECT
    )
    age_limit = models.PositiveIntegerField(null=True)
    performance_limit_type = models.ForeignKey(
        PerformanceLimit, related_name="PerformanceLimit_2", on_delete=models.PROTECT
    )
    performance_limit = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            "test",
            "gender",
            "age_limit_type",
            "age_limit",
            "performance_limit_type",
            "performance_limit",
            "rating",
        )

    def __str__(self):
        return (
            str(self.test)
            + ": "
            + str(self.gender)
            + ": "
            + str(self.age_limit_type)
            + ": "
            + str(self.age_limit)
        )


class WeightGenderPerformanceRating(models.Model):
    test = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    weight_limit_type = models.ForeignKey(
        PerformanceLimit, related_name="WeightPerfLimit_1", on_delete=models.PROTECT
    )
    weight_limit = models.DecimalField(max_digits=5, decimal_places=2)
    performance_limit_type = models.ForeignKey(
        PerformanceLimit, related_name="WeightPerfLimit_2", on_delete=models.PROTECT
    )
    performance_limit = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            "test",
            "gender",
            "weight_limit_type",
            "weight_limit",
            "performance_limit_type",
            "performance_limit",
            "rating",
        )


class BMITestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.PositiveIntegerField()
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class VisceralFatRatingTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.PositiveIntegerField()
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class TheOneMileTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(verbose_name="Weight (kg)")
    one_mile_time = models.DecimalField(decimal_places=2, max_digits=4)
    exercise_heart_rate = models.DecimalField(decimal_places=2, max_digits=5)
    oxygen_consumption = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        verbose_name="Maximal oxygen consumption",
        blank=True,
    )
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class MaximumChestPressTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(verbose_name="Body weight")
    repetition_maximum = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class SixtySecondSitUpTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    no_of_situps = models.PositiveIntegerField()
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class ThePushUpTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    no_of_push_ups = models.PositiveIntegerField(verbose_name="Number of push-ups")
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class SitAndReachTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    reach_in_cm = models.DecimalField(decimal_places=2, max_digits=4)
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class WaistHipRatioTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    waist_measurement = models.PositiveIntegerField()
    hip_measurement = models.PositiveIntegerField()
    waist_hip_ratio = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class BMITest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    height = models.PositiveIntegerField(verbose_name="Height (cm)")
    weight = models.PositiveIntegerField(verbose_name="Weight (kg)")
    bmi = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, verbose_name="Body Mass Index"
    )
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class BodyFatTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    body_fat_percentage = models.PositiveIntegerField()
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class VisceralFatRatingTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    visceral_fat_rating = models.PositiveIntegerField()
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class MuscleMassTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    muscle_mass_percentage = models.DecimalField(decimal_places=2, max_digits=4,verbose_name="Muscle Mass (%)")
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username

class BoneMassTest(models.Model):
    test_date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    weight = models.PositiveIntegerField(verbose_name="Body Weight (kg)")
    bone_mass = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Bone Mass (kg)")
    rating = models.CharField(max_length=256, blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username