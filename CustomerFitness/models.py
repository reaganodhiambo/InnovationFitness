from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserTestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


class TheOneMileTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(verbose_name="Weight (kg)")
    one_mile_time = models.DecimalField(decimal_places=2, max_digits=4)
    exercise_heart_rate = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class MaximumChestPressTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(verbose_name="Body weight")
    repetition_maximum = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class SixtySecondSitUpTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    no_of_situps = models.PositiveIntegerField()

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class ThePushUpTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    no_of_push_ups = models.PositiveIntegerField(verbose_name="Number of push-ups")

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class SitAndReachTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    reach_in_cm = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class WaistHipRatioTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    waist_measurement = models.PositiveIntegerField()
    hip_measurement = models.PositiveIntegerField()

    def __str__(self):
        return self.__name__ + ": " + self.customer.user.username


class BMITest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    height = models.PositiveIntegerField(verbose_name="Height (cm)")
    weight = models.PositiveIntegerField(verbose_name="Weight (kg)")

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class BodyFatTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    body_fat_percentage = models.PositiveIntegerField()

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class VisceralFatRatingTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    visceral_fat_rating = models.PositiveIntegerField()

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


class MuscleMassTest(models.Model):
    customer = models.ForeignKey(UserTestProfile, on_delete=models.DO_NOTHING)
    age = models.PositiveIntegerField()
    muscle_mass_percentage = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.__class__.__name__ + ": " + self.customer.user.username


