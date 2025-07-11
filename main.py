import json
import os
from datetime import datetime
from crewai import Crew
from agents.nutritionist import nutritionist
from agents.trainer import trainer
from agents.psychologist import psychologist
from agents.coach import coach
from tasks.planning_tasks import nutrition_task, trainer_task, psychologist_task, coach_task

# Run Crew
crew = Crew(
    agents=[nutritionist, trainer, psychologist, coach],
    tasks=[nutrition_task, trainer_task, psychologist_task, coach_task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()

    # Save report with timestamped filename
    date_str = datetime.today().strftime("%Y-%m-%d")
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"performance_report_{date_str}.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 🏁 Weekly Performance Plan - {date_str}\n\n")
        f.write(str(result))

    print("\n===== FINAL WEEKLY PLAN =====\n")
    print(str(result))
    print(f"\n[✔] Report saved to {report_path}")