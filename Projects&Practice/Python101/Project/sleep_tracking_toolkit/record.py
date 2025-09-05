# Implement a class DailySleepRecord with the following:

# Attributes:
# date: string, e.g., '2025-04-29'
# segments: list of tuples, each of the form (duration, quality_score) where:
# duration is in hours (float)
# quality_score is from 0 - 100 (int or float)
# Methods:
# average_quality(): returns the average of all quality scores, rounded to two decimal places
# total_duration(): returns the sum of all sleep durations, rounded to two decimal places
# is_restful(duration_threshold, quality_threshold): returns True if all segments of the day meet both duration and quality thresholds. Set default values of 7 and 75 for the thresholds respectively
# average_sleep_score(): returns the average computed sleep score (using compute_sleep_score() in utils), rounded to two decimal places
# summary(): returns a dictionary with keys 'date', 'avg_quality', 'total_duration', 'avg_sleep_score', and 'quality_label'

# record.py

from utils import compute_sleep_score, quality_label

class DailySleepRecord:
    def __init__(self, date, segments):
        self.date = date
        self.segments = segments

    def average_quality(self):
        if not self.segments:
            return 0.0
        sum_quality = sum(quality_score for _, quality_score in self.segments)
        avg_quality = sum_quality / len(self.segments)
        return round(avg_quality, 2)
        
    def total_duration(self):
        if not self.segments:
            return 0.0
        total_duration = sum(duration for duration, _ in self.segments)
        return round(total_duration, 2)

    def is_restful(self, duration_threshold=7, quality_threshold=75):
        return all(duration >= duration_threshold and quality_score >= quality_threshold for duration, quality_score in self.segments)
        
    def average_sleep_score(self):
        if not self.segments:
            return 0.0
        scores = [compute_sleep_score(duration, quality_score) for duration, quality_score in self.segments]
        avg_score = sum(scores) / len(scores)
        return round(avg_score, 2)

    def summary(self):
        avg_quality = self.average_quality()
        total_duration = self.total_duration()
        avg_sleep_score = self.average_sleep_score()
        label = quality_label(avg_sleep_score)

        return {
            'date': self.date,
            'avg_quality': avg_quality,
            'total_duration': total_duration,
            'avg_sleep_score': avg_sleep_score,
            'quality_label': label
        }
