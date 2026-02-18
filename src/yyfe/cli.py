from __future__ import annotations

import argparse
from pathlib import Path

from yyfe.core.policy import Policy
from yyfe.core.runner import run


def main() -> int:
    ap = argparse.ArgumentParser(prog="yyfe", description="YY-FE v0.1 lab engine")
    ap.add_argument("--policy", default="policy.json", help="Path to policy.json")
    ap.add_argument("cmd", choices=["golden"], help="Command to run")
    args = ap.parse_args()

    _ = Policy.load(args.policy)

    if args.cmd == "golden":
        r = run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(Path("tools") / "golden.ps1"),
            ]
        )
        print(r.stdout, end="")
        if not r.ok:
            print(r.stderr, end="")
        return r.exit_code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
