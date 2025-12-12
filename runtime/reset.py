from __future__ import annotations
from pathlib import Path
import shutil

def reset_environment(profile: str, vars: dict[str, str]) -> None:
    desktop = Path(vars["DESKTOP"])
    home = Path(vars["HOME"])
    downloads = home / "Downloads"

    # Remove the benchmark workspace on Desktop
    test_dir = desktop / "AgentX_Test"
    if test_dir.exists():
        shutil.rmtree(test_dir, ignore_errors=True)

    # Remove known test artifacts from Downloads
    for name in ["downloaded_asset.txt", "asset.txt", "downloaded.txt"]:
        p = downloads / name
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass

