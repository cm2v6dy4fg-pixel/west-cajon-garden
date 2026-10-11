---
description: What to plant, start or harvest now and in the coming weeks
argument-hint: "[weeks] [--date YYYY-MM-DD]"
allowed-tools: Bash(python3:*)
---

Here is the garden calendar from this repo's `crops.json` and the station's frost dates:

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/whats_next.py" $ARGUMENTS`

Turn this into a short to-do list for the gardener. Group it into "Do this week" and "Coming up",
lead with anything that closes soon, and mention a frost warning first if there is one. Keep crop
tips from `crops.json` only where they help with the task at hand. Don't invent dates; use the ones above.
