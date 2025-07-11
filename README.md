# Digital Athlete Hub 🧠🏃‍♂️🥦

This project simulates a high-performance digital coaching system using multiple AI agents coordinated via [CrewAI](https://github.com/crewAIInc/crewAI). Each agent is specialized in one of the pillars of sports performance: nutrition, training, mental recovery, and integrated planning.

---

## 🚀 AI Agents

- **🥦 Nutritionist** – Builds nutrition and supplementation plans based on energy expenditure, body composition, and training load.
- **🏋️ Trainer** – Designs weekly training programs using TRIMP, VO2max, intensity, and movement data.
- **🧘 Psychologist** – Prescribes mental recovery strategies from HRV, sleep quality, stress, and body battery.
- **📋 Coach** – Synthesizes all expert recommendations, resolves conflicts, and delivers a unified action plan.

---

## 📥 Input Format

The system uses `garmin_input.json`, generated automatically, with this structure:

```json
{
  "date": "2025-07-11",
  "biometrics": {
    "weight_kg": 72.5,
    "body_fat_percent": 14.3,
    "muscle_mass_kg": 56.1,
    "vo2max": 58,
    "resting_heart_rate": 48
  },
  "training": {
    "load_7d": 3200,
    "avg_intensity": 7.2
  },
  "recovery": {
    "sleep_score": 78,
    "avg_overnight_hrv": 68,
    "body_battery_change": 86,
    "avg_stress": 23,
    "hrv_status": "BALANCED",
    "deep_sleep_sec": 5200,
    "rem_sleep_sec": 4300
  },
  "energy": {
    "total_kcal": 2920,
    "active_kcal": 960,
    "bmr_kcal": 1960
  },
  "activity_summary": {
    "steps": 11200,
    "distance_m": 9250,
    "intensity_minutes": 68
  }
}
```

---

## 🛠️ How to Use

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your credentials:
```ini
GARMIN_USER="<your_garmin_email>"
GARMIN_PASS="<your_garmin_password>"
OPENAI_API_KEY=<your_openai_api_key>
```

3. Export Garmin data:
```bash
python scripts/garmin_export.py
```

4. Parse data to DTO:
```bash
python scripts/parse_garmin_csv_to_dto.py
```

5. Run the agents:
```bash
python main.py
```

The final report will be saved to:
```
reports/performance_report_YYYY-MM-DD.md
```

---

## 📦 Project Structure

```
📁 data/
 ├─ garmin/                  # Raw CSVs exported from API
 ├─ debug/                   # Raw JSON dumps (for inspection)
 └─ garmin_input.json        # Final DTO consumed by agents

📁 agents/
 ├─ nutritionist.py
 ├─ trainer.py
 ├─ psychologist.py
 └─ coach.py

📁 scripts/
 ├─ garmin_export.py         # Fetches data from Garmin API
 └─ parse_garmin_csv_to_dto.py  # Builds unified DTO from CSVs

main.py                      # Coordinates agents via CrewAI
planning_tasks.py            # Shared task definitions for modularity
```

---

## ✏️ How to Customize Agents

Each agent is defined in the `agents/` folder and can be fully customized:
- `role`: the agent's name or specialization
- `goal`: what the agent is expected to optimize
- `backstory`: context that enhances responses and domain relevance

Example (in `trainer.py`):
```python
trainer = Agent(
    role="Strength Coach",
    goal="Improve muscle mass and hypertrophy in beginner athletes",
    backstory="Expert in gym-based progressive overload and recovery."
)
```

---

## 🔜 Roadmap

- 📊 Interactive UI with Streamlit
- 🧠 Weekly feedback based on adherence
- 🧪 Anomaly detection: chronic stress, overtraining, caloric deficit
- 🔄 Support for wearables beyond Garmin (e.g. Polar, Fitbit, Apple Watch)
- 💬 Coach agent can interactively query the user if important data is missing (e.g. weight, fat %, etc.)

---

Powered by **Garmin + CrewAI + Python ❤️**
