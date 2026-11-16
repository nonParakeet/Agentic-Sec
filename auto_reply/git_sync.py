"""Stage, commit, and push project changes for the configured Git remote."""

from __future__ import annotations

import subprocess
from datetime import datetime


def _run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        capture_output=True,
    )


def main() -> int:
    _run_git("add", "-A")

    staged_changes = _run_git("diff", "--cached", "--quiet", check=False)
    if staged_changes.returncode == 1:
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
        _run_git("commit", "-m", f"Auto-sync: {timestamp}")
    elif staged_changes.returncode != 0:
        staged_changes.check_returncode()

    _run_git("push", "origin", "HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
