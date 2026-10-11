# West Cajon Garden

Planting and harvest calendar for a high-desert garden in Phelan, CA, built from the
West Cajon Ambient Weather station's own frost dates and weather history.

- **Live page:** https://cm2v6dy4fg-pixel.github.io/west-cajon-garden/ (current conditions load live from the station)
- **Calendar feed:** https://cm2v6dy4fg-pixel.github.io/west-cajon-garden/garden.ics (subscribe in Google Calendar → Other calendars → From URL)
- **Garden chat:** https://claude.ai/artifact/Mne7tpPjZjDPy2MYCRkvVm

## How it updates

`.github/workflows/weekly.yml` runs every Sunday. It runs `build_garden.py`, which pulls data from the
station's public Ambient Weather share link (no API keys). It then rebuilds the page and the calendar feed,
and publishes them to GitHub Pages. `data/station.json` keeps each week's snapshot.

## Files

- `build_garden.py`: fetches station data and builds the page and `.ics` feed
- `garden.src.html`: page template
- `crops.json`: crops and planting windows. Offsets are in weeks from last spring frost (`L`) or first fall frost (`F`), or fixed `MM-DD` dates.
