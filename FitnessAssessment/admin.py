from django.contrib import admin
from .models import *

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "gender",
        "age",
    )

    search_fields = ("first_name", "last_name")
    ordering = ("first_name", "last_name")


class FitnessTestAdmin(admin.ModelAdmin):
    list_display = ("test_name", "category")


class AgeBucketingAdmin(admin.ModelAdmin):
    list_display = ("test_name", "min_age", "max_age")
    list_filter = ("min_age", "max_age", "test_name")


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
    list_filter = ("gender","min_age", "max_age")


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
    list_display = ("test_date", "customer", "rating", "score")


class PerformanceRatingScoringAdmin(admin.ModelAdmin):
    list_display = ("test_name", "rating", "score")
    list_filter = ("test_name", "rating")


class PerformanceInputAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "test_id",
        "test_date",
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(TestInput)
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(FitnessTest, FitnessTestAdmin)
admin.site.register(AgeBucketing, AgeBucketingAdmin)
admin.site.register(PerformanceRatingScoring, PerformanceRatingScoringAdmin)
admin.site.register(PerformanceLimit)
admin.site.register(OneMileTestPerformance, OneMileTestPerformanceAdmin)
admin.site.register(MaximumChestPressPerformance, MaximumChestPressPerformanceAdmin)
admin.site.register(SixtySecSitUpTestPerformance)
admin.site.register(ThePushUpTestPerformance)
admin.site.register(SitAndReachTestPerformance)
admin.site.register(WaistHipRatioTestPerformance)
admin.site.register(BMITestPerformance)
admin.site.register(BodyFatTestPerformance)
admin.site.register(VisceralFatRatingTestPerformance)
admin.site.register(BoneMassTestPerformance)
admin.site.register(TestPerformance, TestPerformanceAdmin)
admin.site.register(PerformanceInput,PerformanceInputAdmin)
