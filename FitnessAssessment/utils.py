def calculate_one_mile_test(weight, age, gender, time, heart_rate):
    gender_value = 1 if gender.lower() == "male" else 0
    weight_in_pounds = weight * 2.205
    vo2_max = (
        132.853
        - (0.0769 * weight_in_pounds)
        - (0.3877 * age)
        + (6.315 * gender_value)
        - (3.2649 * float(time))
        - (0.1565 * float(heart_rate))
    )
    return vo2_max


def calculate_max_chest_press(weight, repetition_maximum):
    weight_in_pounds = weight * 2.205
    max_chest_press = repetition_maximum / weight_in_pounds
    return max_chest_press



