from __future__ import annotations
import time

class ActionAPI:
  # You will implement these using your chosen computer-use backend.
  def screenshot(self) -> bytes: ...
  def click(self, x: int, y: int) -> None: ...
  def type_text(self, text: str) -> None: ...
  def hotkey(self, *keys: str) -> None: ...
  def wait(self, sec: float) -> None: ...

class DeskPilotBasics:
  def __init__(self, actions: ActionAPI, llm=None):
    self.actions = actions
    self.llm = llm  # optional

  def solve(self, instruction: str, deadline: float) -> None:
    plan = self._plan(instruction)
    for step in plan:
      if time.time() > deadline:
        return
      self._do(step)

  def _plan(self, instruction: str) -> list[str]:
    # Beginner track: start rule-based; later upgrade with an LLM planner.
    i = instruction.lower()
    steps = []
    if "create a folder" in i and "agentx_test" in i:
      steps = ["open_file_explorer", "go_desktop", "make_folder:AgentX_Test"]
    elif "create notes.txt" in i:
      steps = ["open_text_editor", "type_exact:hello agentbeats", "save_file:notes.txt:Desktop/AgentX_Test"]
    else:
      steps = ["fallback_llm_or_manual"]
    return steps

  def _do(self, step: str) -> None:
    # Stub: replace with real action implementations + OCR anchoring.
    if step == "open_file_explorer":
      self.actions.hotkey("CTRL", "L")  # placeholder
    self.actions.wait(0.2)

