# West Cajon Garden

Planting and harvest calendar for a high-desert garden in Phelan, CA, built from the
West Cajon Ambient Weather station's own frost dates and weather history.

- **Live page:** https://cm2v6dy4fg-pixel.github.io/west-cajon-garden/ (current conditions load live from the station)
- **Calendar feed:** https://cm2v6dy4fg-pixel.github.io/west-cajon-garden/garden.ics (subscribe in Google Calendar → Other calendars → From URL)
- **Garden chat:** https://claude.ai/artifact/Mne7tpPjZjDPy2MYCRkvVm

## How it updates

`.github/workflows/build.yml` runs three times a day (about 6 AM, noon and 5 PM Pacific). It runs `build_garden.py`, which pulls data from the
station's public Ambient Weather share link (no API keys). It then rebuilds the page and the calendar feed,
and publishes them to GitHub Pages. It also pulls an 8-day National Weather Service forecast for Storm watch. `data/station.json` keeps each day's snapshot.

## Claude Code plugin

`plugins/garden` adds garden commands to Claude Code. Install it with:

```
/plugin install garden --marketplace cm2v6dy4fg-pixel/west-cajon-garden
```

Then, inside a checkout of this repo:

- `/garden:whats-next [weeks]`: what to plant, start or harvest now and in the coming weeks
- `/garden:add-crop <crop>`: add or update a crop in `crops.json`
- `/garden:farm-check <idea>`: check a farm idea, plan change or purchase against the site's water, time, income and permit constraints
- A `garden-calendar` skill that explains the `crops.json` format, and a hook that validates `crops.json` after each edit
- A `farm-knowledge` skill with the farm's site facts, the owner's decisions, ten design rules and a reference library
  (keyline and Regrarians, permaculture, restoration agriculture, KNF/JADAM, Fukuoka, agroforestry, soil health,
  dryland water harvesting, livestock and bees, farm business, California and county rules). Claude uses it for any
  question about the farm's layout, water, trees, animals, soil, income, permits or funding.
- `scripts/farm_math.py`: hauled-water cost, roof and land runoff, microcatchment (C:CA) sizing, and net $ per 1,000 gal

The garden chat also gets `farm.md`, a short public-safe brief of the farm plan (site, the owner's decisions, design
rules, ranked plan changes, permits). Edit that file when the plan changes; the next build carries it into the chat.

The garden chat page on claude.ai can't fetch the station itself. Each build saves the finished page as
`data/chat.html`, and a scheduled Claude routine republishes it to the chat page once a day (6:40 AM Pacific). The page's
**Refresh data** button (on claude.ai, through the Claude Code Remote connector) runs the same routine on demand.
(`python3 build_garden.py --offline` rebuilds `garden.html` from the saved data without fetching.)

## Files

- `build_garden.py`: fetches station data and builds the page and `.ics` feed
- `garden.src.html`: page template
- `crops.json`: crops and planting windows. Offsets are in weeks from last spring frost (`L`) or first fall frost (`F`), or fixed `MM-DD` dates.
