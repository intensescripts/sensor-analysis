"""Sensor Data Analysis Tool: simulate, analyze and plot sensor readings."""
import csv
import random

import numpy as np
import matplotlib.pyplot as plt

def ask_text(prompt):
    #"""Keep asking until the user enters some text (not empty)."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Invalid input: please enter some text.")


def ask_positive_int(prompt):
    #"""Keep asking until the user enters a whole number greater than 0."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print(f"Invalid input: '{text}' is not a whole number.")
            continue
        if value <= 0:
            print("Invalid input: the number must be greater than 0.")
            continue
        return value

def ask_float(prompt):
    #"""Keep asking until the user enters a number."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print(f"Invalid input: '{text}' is not a number.")

def get_user_input():
    #"""Ask for all settings and return them as a tuple."""
    sensor_type = ask_text("Sensor type (e.g. temperature, light): ")
    count = ask_positive_int("Number of readings: ")

    while True:
        minimum = ask_float("Minimum value: ")
        maximum = ask_float("Maximum value: ")
        if minimum < maximum:
            break
        print("Invalid input: the minimum must be smaller than the maximum. Try again.")

    threshold = ask_float("Alert threshold: ")
    return sensor_type, count, minimum, maximum, threshold

SEED = 42   # fixed seed: the same "random" readings every run (reproducible)

def generate_readings(count, minimum, maximum, seed=SEED):
    #"""Return a NumPy array of count random readings between minimum and maximum."""
    if count <= 0:
        raise ValueError("count must be greater than 0")
    if minimum >= maximum:
        raise ValueError("minimum must be smaller than maximum")

    random.seed(seed)
    readings = [round(random.uniform(minimum, maximum), 2) for _ in range(count)]
    return np.array(readings)

def calculate_statistics(readings):
    """Return a dictionary with the count, mean, minimum, maximum and standard deviation."""
    return {
        "count": readings.size,
        "mean": np.mean(readings),
        "minimum": np.min(readings),
        "maximum": np.max(readings),
        "std": np.std(readings),
    }


def find_outliers(readings, threshold):
    """Return the readings that are above the alert threshold."""
    return readings[readings > threshold]

def print_report(sensor_type, statistics, outliers, threshold):
    #"""Print the statistics and the readings above the threshold."""
    print(f"\n--- {sensor_type} readings ---")
    print(f"Number of readings: {statistics['count']}")
    print(f"Mean:               {statistics['mean']:.2f}")
    print(f"Minimum:            {statistics['minimum']:.2f}")
    print(f"Maximum:            {statistics['maximum']:.2f}")
    print(f"Standard deviation: {statistics['std']:.2f}")
    print(f"Readings above {threshold}: {outliers.size}")
    if outliers.size > 0:
        print("Values above the threshold:", outliers)

def main():
    print("Sensor Data Analysis Tool")
    sensor_type, count, minimum, maximum, threshold = get_user_input()

    readings = generate_readings(count, minimum, maximum)
    statistics = calculate_statistics(readings)
    outliers = find_outliers(readings, threshold)
    print_report(sensor_type, statistics, outliers, threshold)


if __name__ == "__main__":
    main()