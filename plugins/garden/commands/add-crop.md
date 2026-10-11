---
description: Add a crop (or fix one) in crops.json
argument-hint: "<crop name and any details>"
---

Add this crop to `crops.json`: $ARGUMENTS

Use the garden-calendar skill for the entry format. Then:

1. If a crop with the same or a very similar name exists, update it instead of adding a duplicate.
2. Pick windows for this high-desert site (Phelan, CA, about 4,355 ft; hot dry summers, cold windy
   nights). Express them as weeks from last spring frost (`L`) or first fall frost (`F`) unless the
   timing is truly calendar-fixed.
3. Insert it next to crops of the same category, matching the file's existing formatting (1-space indent).
4. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_crops.py"` and fix any problems.
5. Show the new entry and the actual dates it gives this year:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/whats_next.py" 52 | grep -i "<crop name>"`
