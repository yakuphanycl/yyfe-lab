from __future__ import annotations

import argparse
from pathlib import Path

from yyfe.core.policy import Policy
from yyfe.core.runner import run


def main() -> int:
    ap = argparse.ArgumentParser(prog="yyfe", description="YY-FE v0.1 lab engine")
    ap.add_argument("--policy", default="policy.json", help="Path to policy.json")
    ap.add_argument("--out", default="output/plan.json", help="(plan) Path to write plan.json")
    ap.add_argument("--plan", default="output/plan.json", help="(apply) Path to read plan.json")
    ap.add_argument("cmd", choices=["golden", "plan", "apply"], help="Command to run")
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

    if args.cmd == "plan":
        # Create a patch plan (dry-run, just produce a plan artifact)
        import json
        from pathlib import Path

        out_dir = Path("output")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = Path(getattr(args, "out", "output/plan.json"))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # NOTE: adjust these calls if your core API differs.
        # Minimal "plan": for now, just record that we can run golden.
        plan = {
            "version": "0.1",
            "policy_path": str(args.policy),
            "actions": [
                {
                    "id": "golden",
                    "type": "run",
                    "cmd": [
                        "powershell",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        "tools/golden.ps1",
                    ],
                }
            ],
        }

        out_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
        print(f"PLAN_OK: wrote {out_path}")
        return 0

    if args.cmd == "apply":
        import json
        from pathlib import Path

        plan_path = Path(getattr(args, "plan", "output/plan.json"))
        if not plan_path.exists():
            print("APPLY_ERR: missing plan file: {plan_path}. Run `yyfe plan` first (or pass --plan PATH).
            return 2

        plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))

        # --- V0.2 safety: validate plan schema + allowlist ---
        if not isinstance(plan, dict):
            print("APPLY_ERR: plan.json must be an object.")
            return 2

        if plan.get("version") != "0.1":
            print(f"APPLY_ERR: unsupported plan version: {plan.get('version')!r}")
            return 2

        actions = plan.get("actions")
        if not isinstance(actions, list):
            print("APPLY_ERR: actions must be a list.")
            return 2

        # Allowlist ONLY the golden script. Anything else is rejected.
        allowed_cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "tools/golden.ps1",
        ]

        # For now, apply just executes the actions sequentially.
        for a in plan.get("actions", []):
            if not isinstance(a, dict):
                print(f"APPLY_ERR: invalid action entry: {a!r}")
                return 2

            if a.get("type") == "run":
                cmd = a.get("cmd")
                if cmd != allowed_cmd:
                    print(f"APPLY_ERR: blocked cmd (not allowlisted): {cmd!r}")
                    return 2
                r = run(cmd)
                print(r.stdout, end="")
                if not r.ok:
                    print(r.stderr, end="")
                    return r.exit_code

        print("APPLY_OK")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

