from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import zipfile

@dataclass
class CheckResult:
  ok: bool
  message: str

def _p(path: str, vars: dict[str, str]) -> Path:
  for k, v in vars.items():
    path = path.replace(f"{{{k}}}", v)
  return Path(path).expanduser().resolve()

def check_path_exists(spec: dict, vars: dict) -> CheckResult:
  p = _p(spec["path"], vars)
  return CheckResult(p.exists(), f"path_exists({p})")

def check_is_directory(spec: dict, vars: dict) -> CheckResult:
  p = _p(spec["path"], vars)
  return CheckResult(p.is_dir(), f"is_directory({p})")

def check_file_contains_exact(spec: dict, vars: dict) -> CheckResult:
  p = _p(spec["path"], vars)
  if not p.exists() or not p.is_file():
    return CheckResult(False, f"missing_file({p})")
  text = p.read_text(encoding="utf-8", errors="replace")
  return CheckResult(text == spec["text"], f"file_exact_match({p})")

def check_zip_contains(spec: dict, vars: dict) -> CheckResult:
  zp = _p(spec["zip_path"], vars)
  expected = spec["expected_paths"]
  if not zp.exists():
    return CheckResult(False, f"missing_zip({zp})")
  with zipfile.ZipFile(zp, "r") as z:
    names = set(z.namelist())
  missing = [e for e in expected if e not in names]
  return CheckResult(len(missing) == 0, f"zip_contains(missing={missing})")

CHECKS = {
  "path_exists": check_path_exists,
  "is_directory": check_is_directory,
  "file_contains_exact": check_file_contains_exact,
  "zip_contains": check_zip_contains,
}

