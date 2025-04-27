def global_urls(request):
    test_urls = {
        "Test Guide": "test-guide",
        "The One Mile Test": "one-mile-test",
        "Maximum Chest Press Test": "chest-press-test",
        "The 60 Second Sit-up Test": "sit-up-test",
        "The Push-up Test": "push-up-test",
        "Sit-and-Reach Test": "sit-and-reach-test",
        "Waist Hip Ratio": "waist-hip-ratio-test",
        "Body Mass Index": "bmi-test",
        "Body Fat": "body-fat-test",
        "Visceral Fat Rating": "visceral-fat-test",
        "Bone Mass": "bone-mass-test",
    }

    return {"test_urls": test_urls}
