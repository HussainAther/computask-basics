from __future__ import annotations
import json, time
from dataclasses import dataclass
from pathlib import Path
from computask.runtime.scoring import CHECKS
from computask.runtime.reset import reset_environment
from runtime.reset import reset_environment

@dataclass
class TaskScore:
  task_id: str
  points_earned: float
  checks: list[dict]

def load_tasks(path: Path) -> dict:
  return json.loads(path.read_text(encoding="utf-8"))

def run_benchmark(tasks_json: Path, purple_client) -> dict:
  spec = load_tasks(tasks_json)
  vars = {
    "HOME": str(Path.home()),
    "DESKTOP": str(Path.home() / "Desktop"),
  }

  results: list[TaskScore] = []
  total = 0.0
  earned = 0.0

  for task in spec["tasks"]:
    total += float(task.get("points", 1))

    reset_environment(task.get("start_state", {}).get("reset_profile", "clean_basic"), vars)

    instruction = task["instruction"]
    t0 = time.time()
    purple_client.run_task(instruction=instruction, time_limit_sec=task.get("time_limit_sec", 180))
    elapsed = time.time() - t0

    check_reports = []
    ok_all = True
    for chk in task["checks"]:
      fn = CHECKS[chk["type"]]
      r = fn(chk, vars)
      check_reports.append({"type": chk["type"], "ok": r.ok, "message": r.message})
      ok_all = ok_all and r.ok

    pts = float(task.get("points", 1)) if ok_all else 0.0
    earned += pts

    results.append(TaskScore(task_id=task["id"], points_earned=pts, checks=check_reports))

  return {
    "benchmark_id": spec["benchmark_id"],
    "version": spec["version"],
    "total_points": total,
    "earned_points": earned,
    "task_results": [r.__dict__ for r in results],
  }

