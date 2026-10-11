#!/usr/bin/env python3
"""Validate crops.json.

  validate_crops.py [PATH]   check a file (default: ./crops.json); exit 1 on errors
  validate_crops.py --hook   PostToolUse hook mode: read the hook JSON on stdin, check
                             crops.json only if the tool just edited it, exit 2 so Claude
                             sees the errors and fixes them
"""
import json, re, sys, datetime as dt
from pathlib import Path

CATEGORIES = {"veg", "fruit", "herb", "flower", "native", "lawn"}
EVENT_TYPES = {"indoor", "sow", "plant", "harvest", "care", "propagate"}
OFFSET = re.compile(r"^[LF]([+-]\d+)?$")
FIXED = re.compile(r"^(\d\d)-(\d\d)$")


def check_spec(s):
    if OFFSET.match(s):
        return True
    m = FIXED.match(s)
    if not m:
        return False
    try:
        dt.date(2024, int(m[1]), int(m[2]))  # leap year, so 02-29 passes
        return True
    except ValueError:
        return False


def validate(path):
    try:
        crops = json.loads(Path(path).read_text())
    except json.JSONDecodeError as e:
        return [f"not valid JSON: {e}"]
    if not isinstance(crops, list):
        return ["top level must be a list of crops"]
    errors, seen = [], set()
    for i, c in enumerate(crops):
        where = f"crop #{i + 1} ({c.get('n', '?') if isinstance(c, dict) else '?'})"
        if not isinstance(c, dict):
            errors.append(f"{where}: must be an object"); continue
        if not isinstance(c.get("n"), str) or not c["n"].strip():
            errors.append(f"{where}: 'n' (name) is required")
        elif c["n"] in seen:
            errors.append(f"{where}: duplicate name")
        seen.add(c.get("n"))
        if c.get("c") not in CATEGORIES:
            errors.append(f"{where}: 'c' must be one of {sorted(CATEGORIES)}")
        for k in ("tender", "cont"):
            if k in c and c[k] not in (0, 1):
                errors.append(f"{where}: '{k}' must be 0 or 1")
        if "dtm" in c and (not isinstance(c["dtm"], int) or c["dtm"] <= 0):
            errors.append(f"{where}: 'dtm' must be a positive whole number of days")
        if "tip" in c and not isinstance(c["tip"], str):
            errors.append(f"{where}: 'tip' must be a string")
        unknown = set(c) - {"n", "c", "dtm", "tender", "cont", "ev", "tip"}
        if unknown:
            errors.append(f"{where}: unknown keys {sorted(unknown)}")
        ev = c.get("ev")
        if not isinstance(ev, list) or not ev:
            errors.append(f"{where}: 'ev' must be a non-empty list"); continue
        for j, e in enumerate(ev):
            if not isinstance(e, list) or len(e) not in (3, 4):
                errors.append(f"{where} ev[{j}]: must be [type, start, end] or [type, start, end, note]"); continue
            if e[0] not in EVENT_TYPES:
                errors.append(f"{where} ev[{j}]: type '{e[0]}' must be one of {sorted(EVENT_TYPES)}")
            for s in e[1:3]:
                if not isinstance(s, str) or not check_spec(s):
                    errors.append(f"{where} ev[{j}]: '{s}' must be L, F, L+N, F-N (weeks) or MM-DD")
            if len(e) == 4 and not isinstance(e[3], str):
                errors.append(f"{where} ev[{j}]: note must be a string")
    return errors


def main(argv):
    if argv[:1] == ["--hook"]:
        try:
            payload = json.load(sys.stdin)
        except json.JSONDecodeError:
            return 0
        path = (payload.get("tool_input") or {}).get("file_path", "")
        if Path(path).name != "crops.json":
            return 0
        errors = validate(path)
        if errors:
            print("crops.json has problems:\n" + "\n".join(f"- {e}" for e in errors), file=sys.stderr)
            return 2
        return 0
    path = argv[0] if argv else "crops.json"
    errors = validate(path)
    for e in errors:
        print(f"- {e}")
    print(f"{path}: {'OK' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
