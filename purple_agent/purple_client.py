from __future__ import annotations
import time

class PurpleClient:
  """
  Replace this with your real A2A implementation.
  For local testing, this can call your agent directly.
  """
  def __init__(self, agent):
    self.agent = agent

  def run_task(self, instruction: str, time_limit_sec: int = 180) -> None:
    deadline = time.time() + time_limit_sec
    self.agent.solve(instruction, deadline=deadline)

