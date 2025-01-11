from django.contrib import admin
from .models import *

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "age",
    )
    readonly_fields = ("user",)
    search_fields = ("user",)
    ordering = ("user",)


class FitnessTestAdmin(admin.ModelAdmin):
    list_display = ("test_name", "category")


class AgeBucketingAdmin(admin.ModelAdmin):
    list_display = ("test_name", "min_age", "max_age")
    list_filter = ("min_age", "max_age", "test_name")


class AgeGenderPerformanceRatingAdmin(admin.ModelAdmin):
    list_display = (
        "test",
        "gender",
        "age_limit_type",
        "age_limit",
        "performance_limit_type",
        "performance_limit",
        "rating",
    )
    list_filter = (
        "test",
        "gender",
        "age_limit_type",
        "age_limit",
    )


class WeightGenderPerformanceRatingAdmin(admin.ModelAdmin):
    list_display = (
        "test",
        "gender",
        "weight_limit_type",
        "weight_limit",
        "performance_limit_type",
        "performance_limit",
        "rating",
    )
    list_filter = (
        "test",
        "gender",
        "weight_limit_type",
        "weight_limit",
    )


class OneMileTestPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "gender",
        "min_age",
        "max_age",
        "limit_type",
        "performance",
        "rating",
    )
    list_filter = ("gender", "min_age", "max_age")


class WaistHipRatioTestPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "gender",
        "min_age",
        "max_age",
        "limit_type",
        "performance",
        "rating",
    )
    list_filter = ("gender", "min_age", "max_age")


class MaximumChestPressPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "gender",
        "min_age",
        "max_age",
        "performance",
        "rating",
    )
    list_filter = ("gender", "rating")


class TestPerformanceAdmin(admin.ModelAdmin):
    list_display = ("test", "test_date", "customer", "rating", "score")
    list_filter = ("test", "test_date", "rating")


class SixtySecSitUpTestPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "gender",
        "min_age",
        "max_age",
        "limit_type",
        "performance",
    )
    list_filter = ("gender", "performance")


class PerformanceRatingScoringAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "rating",
        "score",
    )
    list_filter = ("test_name", "rating")


class PerformanceInputAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "test_id",
        "test_date",
    )


class VisceralFatRatingTestPerformanceAdmin(admin.ModelAdmin):
    list_display = ("test_name", "rating", "limit_type", "performance")


class BMITestPerformanceAdmin(admin.ModelAdmin):
    list_display = ("test_name", "rating", "limit_type", "performance")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TestInput)
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(FitnessTest, FitnessTestAdmin)
admin.site.register(AgeBucketing, AgeBucketingAdmin)
admin.site.register(PerformanceRatingScoring, PerformanceRatingScoringAdmin)
admin.site.register(PerformanceLimit)
admin.site.register(AgeGenderPerformanceRating, AgeGenderPerformanceRatingAdmin)
admin.site.register(WeightGenderPerformanceRating, WeightGenderPerformanceRatingAdmin)
admin.site.register(OneMileTestPerformance, OneMileTestPerformanceAdmin)
admin.site.register(MaximumChestPressPerformance, MaximumChestPressPerformanceAdmin)
admin.site.register(SixtySecSitUpTestPerformance, SixtySecSitUpTestPerformanceAdmin)
admin.site.register(ThePushUpTestPerformance)
admin.site.register(SitAndReachTestPerformance)
admin.site.register(WaistHipRatioTestPerformance, WaistHipRatioTestPerformanceAdmin)
admin.site.register(BMITestPerformance, BMITestPerformanceAdmin)
admin.site.register(BodyFatTestPerformance)
admin.site.register(
    VisceralFatRatingTestPerformance, VisceralFatRatingTestPerformanceAdmin
)
admin.site.register(TestPerformance, TestPerformanceAdmin)
admin.site.register(PerformanceInput, PerformanceInputAdmin)
