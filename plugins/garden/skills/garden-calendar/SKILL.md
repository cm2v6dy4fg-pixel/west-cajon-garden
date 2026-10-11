---
name: garden-calendar
description: Format and planting math for the West Cajon garden's crops.json. Use when reading, adding or changing crops, planting windows or harvest dates in the west-cajon-garden repo, or when asked when to plant something there.
---

# West Cajon garden calendar

`crops.json` is a list of crops. `build_garden.py` turns it into the page and the `.ics` feed,
using frost dates measured by the station (`data/station.json` → `frost.lastSpring`, `frost.firstFall`).

## Crop entry

```json
{
 "n": "Tomatoes",
 "c": "veg",
 "dtm": 75,
 "tender": 1,
 "cont": 1,
 "ev": [
  ["indoor", "L-7", "L-5"],
  ["plant", "L+2", "L+4"],
  ["propagate", "L+7", "L+11", "Optional note shown instead of the tip."]
 ],
 "tip": "Shade cloth over 95°F helps fruit set."
}
```

| Key | Required | Meaning |
|---|---|---|
| `n` | yes | Display name, unique |
| `c` | yes | `veg`, `fruit`, `herb`, `flower`, `native` or `lawn` |
| `ev` | yes | Windows: `[type, start, end]` or `[type, start, end, note]` |
| `dtm` | no | Days to maturity. With no `harvest` window, harvest is computed from `sow`/`plant` + `dtm` |
| `tender` | no | `1` if frost kills it: computed harvest stops at first fall frost |
| `cont` | no | `1` if it keeps producing: computed harvest runs to first fall frost (+3 weeks if not tender) |
| `tip` | no | One-line advice for this site |

Event types: `indoor` (start indoors), `sow`, `plant` (plant out), `harvest` (shown as "Bloom begins"
for `flower`/`native`), `care`, `propagate`.

Window bounds:
- `L`, `L+2`, `L-6`: weeks from last spring frost
- `F`, `F-4`, `F+1`: weeks from first fall frost
- `06-10`: a fixed month-day, for things that follow day length rather than frost

Windows may wrap the new year (e.g. `F-4` to `L-8` for overwintering crops).

## Checking work

- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_crops.py"` checks the file (the plugin's hook also runs it after every edit).
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/whats_next.py" 52` lists real dates for the next year.
- Tender crops shouldn't be planted out before `L+1`; nights above 50°F matter for peppers and eggplant.
