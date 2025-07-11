import os
import datetime
import json
import pandas as pd
from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()
DAYS_BACK = 7
ACTIVITY_COUNT = 10

def safe_get(d, *keys):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d

def get_avg_hrv_from_array(hrv_data):
    if isinstance(hrv_data, list) and len(hrv_data) > 0:
        values = [item.get("value") for item in hrv_data if item.get("value") is not None]
        if values:
            return round(sum(values) / len(values), 1)
    return None

def get_garmin_data():
    try:
        client = Garmin(os.getenv("GARMIN_USER"), os.getenv("GARMIN_PASS"))
        client.login()
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None, None

    try:
        today = datetime.date.today()
        start = today - datetime.timedelta(days=DAYS_BACK)
        wellness_records = []

        for i in range(DAYS_BACK):
            date = (start + datetime.timedelta(days=i)).isoformat()
            stats = client.get_stats(date)
            body = client.get_body_composition(date)
            sleep = client.get_sleep_data(date)

            hrv_array = safe_get(sleep, "hrvData")
            avg_hrv = get_avg_hrv_from_array(hrv_array)

            moderate = safe_get(stats, "moderateIntensityMinutes") or 0
            vigorous = safe_get(stats, "vigorousIntensityMinutes") or 0

            record = {
                "date": date,
                # Biometria
                "weight": safe_get(body, "weight"),
                "bodyFat": safe_get(body, "bodyFat"),
                "muscleMass": safe_get(body, "muscleMass"),
                # Cardio / Stress
                "restingHeartRate": safe_get(stats, "restingHeartRate"),
                "heartRateVariability": avg_hrv or safe_get(stats, "heartRateVariability"),
                "stressLevel": safe_get(stats, "stressLevel") or safe_get(stats, "maxStressLevel"),
                # Sleep
                "sleepScore": safe_get(sleep, "dailySleepDTO", "sleepScores", "overall", "value"),
                "avgOvernightHrv": safe_get(sleep, "avgOvernightHrv"),
                "bodyBatteryChange": safe_get(sleep, "bodyBatteryChange"),
                "sleepDuration": safe_get(sleep, "dailySleepDTO", "sleepTimeSeconds"),
                "deepSleep": safe_get(sleep, "dailySleepDTO", "deepSleepSeconds"),
                "remSleep": safe_get(sleep, "dailySleepDTO", "remSleepSeconds"),
                "hrvStatus": safe_get(sleep, "hrvStatus"),
                # Calories
                "totalKilocalories": safe_get(stats, "totalKilocalories"),
                "activeKilocalories": safe_get(stats, "activeKilocalories"),
                "bmrCalories": safe_get(stats, "bmrCalories"),
                # Activity
                "intensityMinutes": moderate + vigorous,
                "steps": safe_get(stats, "wellnessSteps") or safe_get(stats, "steps"),
                "distance": safe_get(stats, "wellnessDistanceMeters") or safe_get(stats, "distance")
            }
            wellness_records.append(record)

        activities = client.get_activities(0, ACTIVITY_COUNT)
        return wellness_records, activities

    except Exception as e:
        print(f"[ERROR] Failed to fetch data from Garmin: {e}")
        return None, None

def save_to_csv(wellness_data, activities):
    output_dir = "data/garmin"
    os.makedirs(output_dir, exist_ok=True)

    df_wellness = pd.DataFrame(wellness_data)
    df_wellness.dropna(how='all', subset=df_wellness.columns[1:], inplace=True)
    df_wellness.to_csv(f"{output_dir}/garmin_wellness.csv", index=False)

    activity_list = []
    for a in activities:
        activity_list.append({
            "date": a.get("startTimeLocal"),
            "activity_type": safe_get(a, "activityType", "typeKey"),
            "distance": a.get("distance"),
            "duration": a.get("duration"),
            "calories": a.get("calories"),
            "averageHR": a.get("averageHR"),
            "maxHR": a.get("maxHR"),
            "vo2max": a.get("vO2MaxValue"),
            "training_effect_aerobic": a.get("aerobicTrainingEffect"),
            "training_effect_anaerobic": a.get("anaerobicTrainingEffect"),
            "averageSpeed": a.get("averageSpeed")
        })

    df_activities = pd.DataFrame(activity_list)
    df_activities.to_csv(f"{output_dir}/garmin_activities.csv", index=False)

if __name__ == "__main__":
    wellness, activities = get_garmin_data()
    if wellness and activities:
        save_to_csv(wellness, activities)
        print("[✔] Garmin data exported to data/garmin/")
    else:
        print("[✘] Failed to export data from Garmin.")