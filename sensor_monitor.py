"""Sensor Data Analysis Tool: simulate, analyze and plot sensor readings."""
import csv
import random

import numpy as np
import matplotlib.pyplot as plt


def ask_text(prompt):
    """Keep asking until the user enters some text (not empty)."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Invalid input: please enter some text.")


def ask_positive_int(prompt):
    """Keep asking until the user enters a whole number greater than 0."""
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
    """Keep asking until the user enters a number."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print(f"Invalid input: '{text}' is not a number.")


def get_user_input():
    """Ask for all settings and return them as a tuple."""
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


SEED = 42
def generate_readings(count, minimum, maximum, seed=SEED):
    """Return a NumPy array of count random readings between minimum and maximum."""
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
    """Print the statistics and the readings above the threshold."""
    print(f"\n--- {sensor_type} readings ---")
    print(f"Number of readings: {statistics['count']}")
    print(f"Mean:               {statistics['mean']:.2f}")
    print(f"Minimum:            {statistics['minimum']:.2f}")
    print(f"Maximum:            {statistics['maximum']:.2f}")
    print(f"Standard deviation: {statistics['std']:.2f}")
    print(f"Readings above {threshold}: {outliers.size}")
    if outliers.size > 0:
        print("Values above the threshold:", outliers)


CSV_FILE = "readings.csv"
def save_readings(filename, readings, sensor_type):
    """Save the readings to a CSV file: sample number, sensor type, reading."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["sample", "sensor_type", "reading"])
        for sample_number, value in enumerate(readings, start=1):
            writer.writerow([sample_number, sensor_type, value])


def load_readings(filename):
    """Load readings from a CSV file. Return (sensor_type, NumPy array of readings)."""
    readings = []
    sensor_type = "unknown"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            readings.append(float(row["reading"]))
            sensor_type = row.get("sensor_type", sensor_type)
    if not readings:
        raise ValueError(f"{filename} contains no readings")
    return sensor_type, np.array(readings)


def plot_readings(readings, threshold, sensor_type):
    """Line plot of the readings with the alert threshold. Saves it as line_plot.png."""
    sample_numbers = np.arange(1, readings.size + 1)
    above = readings > threshold

    plt.figure(figsize=(10, 4))
    plt.plot(sample_numbers, readings, marker="o", markersize=3, label=f"{sensor_type} reading")
    plt.plot(sample_numbers[above], readings[above], "o", color="red", label="Above threshold")
    plt.axhline(threshold, color="red", linestyle="--", label=f"Alert threshold ({threshold})")
    plt.title(f"{sensor_type.capitalize()} readings")
    plt.xlabel("Sample number")
    plt.ylabel(f"{sensor_type} value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("line_plot.png", dpi=150)


def plot_histogram(readings, threshold, sensor_type):
    """Histogram of the readings with the alert threshold. Saves it as histogram.png."""
    plt.figure(figsize=(8, 4))
    plt.hist(readings, bins=10, edgecolor="black", label=f"{sensor_type} readings")
    plt.axvline(threshold, color="red", linestyle="--", label=f"Alert threshold ({threshold})")
    plt.title(f"Distribution of {sensor_type} readings")
    plt.xlabel(f"{sensor_type} value")
    plt.ylabel("Number of readings")
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("histogram.png", dpi=150)


def ask_choice():
    """Ask whether to generate new readings or load them from a CSV file."""
    print("1) Generate new sensor readings")
    print("2) Load readings from a CSV file")
    while True:
        choice = input("Choose 1 or 2: ").strip()
        if choice in ("1", "2"):
            return choice
        print("Invalid input: please type 1 or 2.")


def analyze_and_plot(sensor_type, readings, threshold):
    """Print the statistics and readings above the threshold, then show both graphs."""
    statistics = calculate_statistics(readings)
    outliers = find_outliers(readings, threshold)
    print_report(sensor_type, statistics, outliers, threshold)
    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, threshold, sensor_type)
    plt.show()


def main():
    print("Sensor Data Analysis Tool")
    choice = ask_choice()

    if choice == "1":
        sensor_type, count, minimum, maximum, threshold = get_user_input()
        readings = generate_readings(count, minimum, maximum)
        try:
            save_readings(CSV_FILE, readings, sensor_type)
            print(f"Saved {readings.size} readings to {CSV_FILE}")
        except OSError as error:
            print(f"Could not save {CSV_FILE}: {error}")
    else:
        filename = input(f"CSV file to load (press Enter for {CSV_FILE}): ").strip() or CSV_FILE
        try:
            sensor_type, readings = load_readings(filename)
        except OSError as error:
            print(f"Could not open {filename}: {error}")
            return
        except (ValueError, KeyError) as error:
            print(f"{filename} is not a valid readings file: {error}")
            return
        print(f"Loaded {readings.size} {sensor_type} readings from {filename}")
        threshold = ask_float("Alert threshold: ")

    analyze_and_plot(sensor_type, readings, threshold)

    
if __name__ == "__main__":
    main()