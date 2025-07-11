import pandas as pd
import os
import json
from datetime import datetime

def load_data():
    base_path = "data/garmin"
    wellness_path = os.path.join(base_path, "garmin_wellness.csv")
    activities_path = os.path.join(base_path, "garmin_activities.csv")

    df_wellness = pd.read_csv(wellness_path)
    df_activities = pd.read_csv(activities_path)
    return df_wellness, df_activities

def build_dto(df_wellness, df_activities):
    latest = df_wellness.iloc[-1]

    # Biometry
    weight = latest.get("weight", None)
    body_fat = latest.get("bodyFat", None)
    muscle_mass = latest.get("muscleMass", None)
    resting_hr = latest.get("restingHeartRate", None)
    vo2max = df_activities["vo2max"].dropna().max()

    # Sleep and Recovery
    sleep_score = latest.get("sleepScore", None)
    avg_hrv = latest.get("avgOvernightHrv", None)
    body_battery = latest.get("bodyBatteryChange", None)
    stress = latest.get("stressLevel", None)
    hrv_status = latest.get("hrvStatus", None)
    deep_sleep = latest.get("deepSleep", None)
    rem_sleep = latest.get("remSleep", None)

    # Calories
    total_kcal = latest.get("totalKilocalories", None)
    active_kcal = latest.get("activeKilocalories", None)
    bmr_kcal = latest.get("bmrCalories", None)

    # Movement
    steps = latest.get("steps", None)
    distance = latest.get("distance", None)
    intensity_minutes = latest.get("intensityMinutes", None)

    # Training
    valid_activities = df_activities.dropna(subset=["duration"])
    valid_activities["duration_min"] = valid_activities["duration"] / 60
    valid_activities["intensity"] = valid_activities["training_effect_aerobic"].fillna(1.0) * 2
    valid_activities["trimp"] = valid_activities["duration_min"] * valid_activities["intensity"]

    load_7d = round(valid_activities["trimp"].sum(), 1)
    avg_intensity = round(valid_activities["intensity"].mean(), 1)

    dto = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "biometrics": {
            "weight_kg": round(weight, 1) if pd.notna(weight) else None,
            "body_fat_percent": round(body_fat, 1) if pd.notna(body_fat) else None,
            "muscle_mass_kg": round(muscle_mass, 1) if pd.notna(muscle_mass) else None,
            "vo2max": round(vo2max, 1) if pd.notna(vo2max) else None,
            "resting_heart_rate": int(resting_hr) if pd.notna(resting_hr) else None
        },
        "training": {
            "load_7d": load_7d,
            "avg_intensity": avg_intensity
        },
        "recovery": {
            "sleep_score": int(sleep_score) if pd.notna(sleep_score) else None,
            "avg_overnight_hrv": int(avg_hrv) if pd.notna(avg_hrv) else None,
            "body_battery_change": int(body_battery) if pd.notna(body_battery) else None,
            "avg_stress": int(stress) if pd.notna(stress) else None,
            "hrv_status": hrv_status if pd.notna(hrv_status) else None,
            "deep_sleep_sec": int(deep_sleep) if pd.notna(deep_sleep) else None,
            "rem_sleep_sec": int(rem_sleep) if pd.notna(rem_sleep) else None
        },
        "energy": {
            "total_kcal": int(total_kcal) if pd.notna(total_kcal) else None,
            "active_kcal": int(active_kcal) if pd.notna(active_kcal) else None,
            "bmr_kcal": int(bmr_kcal) if pd.notna(bmr_kcal) else None
        },
        "activity_summary": {
            "steps": int(steps) if pd.notna(steps) else None,
            "distance_m": int(distance) if pd.notna(distance) else None,
            "intensity_minutes": int(intensity_minutes) if pd.notna(intensity_minutes) else None
        }
    }

    return dto

def save_json(dto):
    output_path = "data/garmin_input.json"
    with open(output_path, "w") as f:
        json.dump(dto, f, indent=2)
    print(f"[✔] DTO saved to {output_path}")

if __name__ == "__main__":
    wellness, activities = load_data()
    dto = build_dto(wellness, activities)
    save_json(dto)
