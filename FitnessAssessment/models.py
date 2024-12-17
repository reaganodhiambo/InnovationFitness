from django.db import models
from django.db.models import When, Case, Value
from django.db.models.functions import Concat, Cast
from datetime import datetime
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    gender = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    phone_number = models.CharField(max_length=256, blank=False,null=True)
    age = models.PositiveIntegerField(blank=False)
    gender = models.CharField(max_length=10, choices=gender)


    class Meta:
        verbose_name = "User Profle"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


class TestInput(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    percentage_body_fat = models.PositiveIntegerField(null=True)
    waist_measurement = models.PositiveIntegerField(null=True)
    hip_measurement = models.PositiveIntegerField(null=True)
    muscle_mass = models.PositiveIntegerField(null=True)
    height_in_cm = models.PositiveIntegerField(null=True)
    weight_in_kg = models.PositiveIntegerField(null=True)
    bone_mass = models.DecimalField(decimal_places=2, max_digits=3, null=True)
    metabolic_age = models.PositiveIntegerField(null=True)
    bmi = models.PositiveIntegerField(null=True)
    visceral_fat_rating = models.PositiveIntegerField(null=True)
    one_mile_time = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    exercise_heart_rate = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    repetition_maximum = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    no_of_situps = models.PositiveIntegerField(null=True)
    no_of_push_ups = models.PositiveIntegerField(null=True)
    sit_and_reach = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    test_date = models.DateField()

    class Meta:
        unique_together = ("customer", "test_date")

    def __str__(self):
        return str(self.customer)


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


class AgeBucketing(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.CASCADE)
    min_age = models.PositiveIntegerField(blank=True, null=True)
    max_age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return (
            str(self.test_name) + ": " + str(self.min_age) + " - " + str(self.max_age)
        )


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
        return str(self.rating)


class PerformanceLimit(models.Model):
    type = models.CharField(max_length=10)
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.type


class OneMileTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=3, decimal_places=1)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class MaximumChestPressPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class SixtySecSitUpTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=3, decimal_places=1)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class ThePushUpTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=3, decimal_places=1)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class SitAndReachTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class WaistHipRatioTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=3, decimal_places=2)
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class BMITestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)
    performance = models.PositiveIntegerField()
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class BodyFatTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)
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


class BoneMassWeightBucketing(models.Model):
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    min_weight = models.PositiveIntegerField(blank=True, null=True)
    max_weight = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return (
            str(self.gender)
            + ": "
            + str(self.min_weight)
            + " - "
            + str(self.max_weight)
        )


class AgeLimit(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.CASCADE)
    age_limit = models.PositiveIntegerField(blank=True, null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)

    def __str__(self):
        return (
            str(self.test_name)
            + ": "
            + str(self.limit_type)
            + ": "
            + str(self.age_limit)
        )


class WeightLimit(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    weight_limit = models.PositiveIntegerField(blank=True, null=True)
    limit_type = models.ForeignKey(PerformanceLimit, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("test_name", "gender", "weight_limit", "limit_type")

    def __str__(self):
        return (
            str(self.test_name)
            + ": "
            + str(self.gender)
            + ": "
            + str(self.limit_type)
            + ": "
            + str(self.weight_limit)
        )


class BoneMassTestPerformance(models.Model):
    test_name = models.ForeignKey(FitnessTest, on_delete=models.PROTECT)
    weight_limit = models.ForeignKey(WeightLimit, on_delete=models.PROTECT)
    performance = models.DecimalField(max_digits=3, decimal_places=2)
    performance_limit_type = models.ForeignKey(
        PerformanceLimit, on_delete=models.PROTECT
    )
    rating = models.ForeignKey(PerformanceRatingScoring, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.test_name)


class TestPerformance(models.Model):
    test_date = models.DateField()
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    test_name = models.ForeignKey(FitnessTest, on_delete=models.DO_NOTHING)
    rating = models.CharField(max_length=50, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        unique_together = ("customer", "test_name", "test_date")

    def __str__(self):
        return str(self.test_date)


class PerformanceInput(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    test_id = models.ForeignKey(FitnessTest, on_delete=models.DO_NOTHING)
    test_date = models.DateTimeField(auto_now=True)
    performance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.customer)
