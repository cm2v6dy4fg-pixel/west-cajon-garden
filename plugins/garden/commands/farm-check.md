---
description: Check a farm idea, plan or purchase against the site's rules and goals
argument-hint: "<idea, plan change or purchase>"
allowed-tools: Bash(python3:*)
---

Check this against the West Cajon farm's goals and design rules: $ARGUMENTS

Use the farm-knowledge skill (read `references/00-site-lens.md`, then only the references this touches). Then:

1. Say in one line whether it fits, fits with changes, or should wait, and why.
2. Water: how many gallons a year it needs and what that costs at $60/1,000 gal hauled. If it earns money, give
   net $ per 1,000 gal and per labour hour with
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/farm_math.py" return <net> <gallons> --hours <h>`. Label estimates.
3. Time: weekly hours and whether they need set times; it has to fit the 4-16 hour week alongside what's planned.
4. Goal: does it cut a household cost or bring in more cash per gallon and per hour than what it replaces?
5. Rules it bumps into (zoning, MWA, CDFA, county, CDFW) from `references/compliance.md`, with "confirm with the
   agency" where money is at stake, and any cost-share (EQIP practice code) that could pay for part of it.
6. Anything in the owner's decisions or `references/plan-changes.md` it conflicts with.

Keep it short and plain. Show the arithmetic you relied on.
