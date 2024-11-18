
def calculate_one_mile_test(weight, age, gender, time, heart_rate):
    # Calculate VO2 Max
    # Args:
    # weight: Weight in pounds.
    # gender: Gender (1 for male, 0 for female).
    # time: Time taken to complete 1 mile in minutes.
    # heart_rate: Exercise heart rate in beats per minute.

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

# calculate_one_mile_test(32,24,"Male",4.654,46)


# muscle strength
# maximum chest press


def calculate_max_chest_press(weight, repetition_maximum):
    # Args
    # rep max in  pounds
    # weight in pounds
    weight_in_pounds = weight * 2.205
    max_chest_press = repetition_maximum / weight_in_pounds
    return max_chest_press
