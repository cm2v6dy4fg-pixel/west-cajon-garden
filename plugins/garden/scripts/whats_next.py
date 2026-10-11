#!/usr/bin/env python3
"""Print what's open in the garden now and what opens soon.

Run from inside a west-cajon-garden checkout:  whats_next.py [WEEKS] [--date YYYY-MM-DD]
Reuses build_garden.calendar_events and the frost dates in data/station.json, so it
matches the live page and the .ics feed.
"""
import json, sys, datetime as dt
from pathlib import Path


def repo_root():
    for d in [Path.cwd(), *Path.cwd().parents]:
        if (d / "build_garden.py").exists() and (d / "crops.json").exists():
            return d
    sys.exit("whats_next: run this inside a west-cajon-garden checkout (no build_garden.py found).")


def main(argv):
    weeks, today = 6, None
    args = iter(argv)
    for a in args:
        if a == "--date":
            today = dt.date.fromisoformat(next(args))
        elif a.isdigit():
            weeks = int(a)
    root = repo_root()
    sys.path.insert(0, str(root))
    from build_garden import calendar_events

    station = json.loads((root / "data" / "station.json").read_text())
    crops = json.loads((root / "crops.json").read_text())
    today = today or dt.date.fromisoformat(station["updated"][:10])
    events = calendar_events(crops, station["frost"], today, horizon_days=weeks * 7, lookback_days=366)

    open_now = [e for e in events if e["date"] <= today.isoformat() <= e["end"]]
    upcoming = [e for e in events if e["date"] > today.isoformat()]
    now_label = lambda e: e["summary"].removeprefix("Garden: ").replace("Harvest begins - ", "Harvest ").replace("Bloom begins - ", "In bloom: ")
    fmt = lambda iso: f"{dt.date.fromisoformat(iso):%b %-d}"
    f = station["frost"]
    print(f"West Cajon garden, {today:%a %b %-d, %Y}")
    print(f"Frost dates from the station: last spring {fmt(f['lastSpring'])}, first fall {fmt(f['firstFall'])}\n")

    print("Open now:")
    for e in sorted(open_now, key=lambda e: e["end"]):
        print(f"  - {now_label(e)} (until {fmt(e['end'])})")
    if not open_now:
        print("  (nothing)")

    print(f"\nOpening in the next {weeks} weeks:")
    for e in upcoming:
        print(f"  - {fmt(e['date'])}: {e['summary'].removeprefix('Garden: ')} (through {fmt(e['end'])})")
    if not upcoming:
        print("  (nothing)")

    cold = [d for d in station.get("forecast", {}).get("days", []) if d.get("low") is not None and d["low"] <= 32]
    if cold:
        nights = ", ".join(f"{fmt(d['d'])} ({d['low']}°F)" for d in cold)
        print(f"\nFrost in the forecast: {nights}. Cover or hold off on tender crops.")


if __name__ == "__main__":
    main(sys.argv[1:])
