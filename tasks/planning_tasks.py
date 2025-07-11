import json
from crewai import Task
from agents.nutritionist import nutritionist
from agents.trainer import trainer
from agents.psychologist import psychologist
from agents.coach import coach
from dotenv import load_dotenv

# Load input data
load_dotenv()
with open("data/garmin_input.json") as f:
    data = json.load(f)

bio = data["biometrics"]
training = data["training"]
recovery = data["recovery"]
energy = data.get("energy", {})
activity = data.get("activity_summary", {})

# Check for missing critical biometrics
missing = []
if bio.get("weight_kg") is None:
    missing.append("weight")
if bio.get("body_fat_percent") is None:
    missing.append("body fat %")
if bio.get("muscle_mass_kg") is None:
    missing.append("muscle mass")

missing_msg = (
    f"Missing data: {', '.join(missing)}. Please update Garmin or insert manually."
    if missing else "All biometrics available."
)

# Tasks for each agent
nutrition_task = Task(
    agent=nutritionist,
    description=(
        f"Design a 7-day nutrition plan based on the athlete's energy expenditure and training load. "
        f"Available data: active kcal: {energy.get('active_kcal')}, BMR: {energy.get('bmr_kcal')}, total kcal: {energy.get('total_kcal')}, "
        f"training load: {training['load_7d']}, intensity: {training['avg_intensity']}. "
        f"Biometrics: weight: {bio.get('weight_kg')}, fat%: {bio.get('body_fat_percent')}, muscle mass: {bio.get('muscle_mass_kg')}"
    ),
    expected_output="A 7-day meal plan with macronutrient targets, hydration and supplement guidelines"
)

trainer_task = Task(
    agent=trainer,
    description=(
        f"Based on a training load of {training['load_7d']} and average intensity {training['avg_intensity']}, "
        f"design a weekly training program. VO2max is {bio.get('vo2max')} and resting HR is {bio.get('resting_heart_rate')}. "
        f"Movement data: steps: {activity.get('steps')}, distance: {activity.get('distance_m')} meters."
    ),
    expected_output="Structured training week with volume, intensity, and zone targets"
)

psychologist_task = Task(
    agent=psychologist,
    description=(
        f"Mental recovery optimization task. Stress level is {recovery.get('avg_stress')}, HRV is {recovery.get('avg_overnight_hrv')}, "
        f"sleep score is {recovery.get('sleep_score')}, body battery change is {recovery.get('body_battery_change')}. "
        f"REM sleep: {recovery.get('rem_sleep_sec')}s, Deep sleep: {recovery.get('deep_sleep_sec')}s, HRV status: {recovery.get('hrv_status')}"
    ),
    expected_output="Mindfulness plan + cognitive recovery strategy tailored to stress/sleep profile"
)

coach_task = Task(
    agent=coach,
    description=(
        "Integrate all expert recommendations into a single coherent plan. Flag missing or inconsistent data such as absent biometrics. "
        f"Context: {missing_msg}"
    ),
    expected_output="Final weekly markdown plan with warnings, priorities and adaptation strategies"
)