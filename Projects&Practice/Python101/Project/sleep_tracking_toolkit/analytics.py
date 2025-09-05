# analytics.py
# Implement the following functions:

# overall_average_duration(records): Given a list of records, it returns the overall average sleep duration across all records. It should calculate one combined average from all readings.
# best_sleep_day(records): Given a list of records, it returns the date of the record with the highest average sleep score
# detect_under_sleep_days(records, threshold): returns a list of dates where any segment has duration below the threshold. It should include a date if at least one reading is below the threshold.
# detect_spike(durations, *, threshold=2): This function checks whether the durations contain a sharp jump or drop between any two consecutive values. It returns True if any two consecutive durations differ by the given threshold or more. The threshold value should be passed by name and have a default.
# duration_trend(durations): returns a list of 'up', 'down', or 'same' describing how the sleep duration changes in the list of durations. The function should compare each duration in the list with the one before it.
# average_sleep_score_across_days(records): returns the average of all segment-level sleep scores (using the proper function already implemented) across all records

# analytics.py

def overall_average_duration(records):
    if not records:
        return 0.0
    sum_duration = sum(duration for duration, _ in records.segments)
    avg_duration = sum_duration / len(records)
    return round(avg_duration, 2)

from record import average_sleep_score

def best_sleep_day(records):
    best_score = None
    best_date = None
    for record in records:
        score = record.average_sleep_score()
        if score > best_score:
            best_score = score
            best_date = record.date
    return best_date


def detect_under_sleep_days(records, threshold=7):
    under_sleep_dates = []
    for record in records:
        for duration, _ in record.segments:
            if duration < threshold:     
                under_sleep_dates.append(record.date)
    return under_sleep_dates


def detect_spike(durations, *, threshold=2):
    for i in range(1, len(durations)):
        if (durations[i] - durations[i - 1]) >= threshold:
            return True
    return False


def duration_trend(durations):
    trend = []
    for i in range(1, len(durations)):
        if durations[i] > durations[i - 1]:
            trend.append("up")
        elif durations[i] < durations[i - 1]:
            trend.append("down")
        else:
            trend.append("same")
    return trend

from utils import compute_sleep_score

def average_sleep_score_across_days(records):
    scores = []
    for record in records:
        for duration, quality_score in record.segments:
            score = compute_sleep_score(duration, quality_score)
            scores.append(score)
    if not scores:
        return 0.0
    avg_sleep_score = sum(scores) / len(scores) 
    return round(avg_sleep_score, 2)
