#!/usr/bin/env python3
"""Pull West Cajon station data from Ambient's public share link and build garden.html.

Run weekly:  python3 build_garden.py
Only public, non-identifying fields are written into the page (no street address or coordinates).
"""
import json, urllib.request, urllib.parse, datetime as dt, time
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

SLUG = "b937402f7843146297e761ffeb631e2a"
BASE = "https://lightning.ambientweather.net"
DASHBOARD = "https://ambientweather.net/dashboard/" + SLUG
HERE = Path(__file__).resolve().parent


def get(url):
    headers = {"User-Agent": "west-cajon-garden/1.0 (github.com/cm2v6dy4fg-pixel/west-cajon-garden)"}
    if "weather.gov" in url:
        headers["Accept"] = "application/geo+json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


LABEL = {"indoor": "Start indoors", "sow": "Sow", "plant": "Plant out", "harvest": "Harvest begins", "care": "Start", "propagate": "Propagate"}
CLAUDE_URL = "https://claude.ai/artifact/Mne7tpPjZjDPy2MYCRkvVm"
SITE_URL = "https://cm2v6dy4fg-pixel.github.io/west-cajon-garden/"
ICS_URL = SITE_URL + "garden.ics"


def label_for(c, t):
    if t == "harvest" and c["c"] in ("flower", "native"):
        return "Bloom begins"
    if t == "sow" and any(w in c["n"] for w in ("Garlic", "Onion", "Potato")):
        return "Plant"
    return LABEL[t]


def calendar_events(crops, frost, today, horizon_days=42, lookback_days=7):
    """Same planting math as the page: offsets in weeks from last spring (L) / first fall (F) frost."""
    year = today.year
    jan0 = dt.date(year, 1, 1) - dt.timedelta(days=1)
    ydays = (dt.date(year, 12, 31) - jan0).days
    doy = lambda m, d: (dt.date(year, m, d) - jan0).days
    md = lambda iso, fb: tuple(map(int, iso.split("-")[1:])) if iso else fb
    L = doy(*md(frost["lastSpring"], (4, 27)))
    F = doy(*md(frost["firstFall"], (11, 1)))

    def spec(s):
        if s[0] in "LF":
            base = L if s[0] == "L" else F
            return base + (int(s[1:]) * 7 if len(s) > 1 else 0)
        m, d = map(int, s.split("-"))
        return doy(m, d)

    t0 = (today - jan0).days
    out = []
    for c in crops:
        evs = []
        has_h = any(e[0] == "harvest" for e in c["ev"])
        for t, a, b, *note in c["ev"]:
            s_, e_ = spec(a), spec(b)
            evs.append((t, s_, e_, note[0] if note else None))
            if not has_h and c.get("dtm") and t in ("sow", "plant"):
                hs = s_ + c["dtm"]
                he = (F if c.get("tender") else F + 21) if c.get("cont") else e_ + c["dtm"] + 21
                if c.get("tender"):
                    he = min(he, F)
                if he > hs:
                    evs.append(("harvest", hs, he, None))
        for i, (t, s_, e_, note) in enumerate(evs):
            for shift in (-ydays, 0, ydays):  # windows that wrap the year, and next year's early windows
                a, b = s_ + shift, e_ + shift
                if t0 - lookback_days <= a <= t0 + horizon_days:
                    start = jan0 + dt.timedelta(days=a)
                    end = jan0 + dt.timedelta(days=b)
                    slug = "".join(ch if ch.isalnum() else "-" for ch in c["n"].lower()).strip("-")
                    title = f"Garden: {label_for(c, t)} {c['n'].lower() if t != 'harvest' else ''}".strip()
                    if t == "harvest":
                        title = f"Garden: {label_for(c, t)} - {c['n']}"
                    elif t == "propagate":
                        title = f"Garden: Propagate - {c['n']}"
                    elif t == "care":
                        title = f"Garden: {c['n']}"
                    else:
                        title = f"Garden: {label_for(c, t)} {c['n']}"
                    desc = f"Window: {start:%b %-d} - {end:%b %-d}."
                    if note:
                        desc += " " + note
                    elif c.get("tip"):
                        desc += " " + c["tip"]
                    desc += f"\n\nWest Cajon garden calendar: {SITE_URL}"
                    out.append({"key": f"{slug}-{t}-{i}-{start.year}", "date": start.isoformat(), "end": end.isoformat(),
                                "type": t, "crop": c["n"], "summary": title, "description": desc})
    out.sort(key=lambda e: (e["date"], e["summary"]))
    return out


def nws_forecast(info, tz):
    """8-day high/low/rain-chance from the National Weather Service (free, no keys). Returns None on any failure,
    and the page then says the forecast needs a refresh instead of showing stale or made-up numbers."""
    try:
        c = ((info.get("coords") or {}).get("coords")) or {}
        point = get(f"https://api.weather.gov/points/{round(c['lat'], 2)},{round(c['lon'], 2)}")["properties"]
        periods = get(point["forecast"])["properties"]["periods"]
        days = {}
        for p in periods:
            d = p["startTime"][:10]
            t = p["temperature"] if p.get("temperatureUnit") == "F" else round(p["temperature"] * 1.8 + 32, 1)
            pop = (p.get("probabilityOfPrecipitation") or {}).get("value") or 0
            day = days.setdefault(d, {"d": d, "high": None, "low": None, "precip": 0})
            day["high" if p["isDaytime"] else "low"] = t
            day["precip"] = max(day["precip"], pop)
        out = [x for x in sorted(days.values(), key=lambda x: x["d"]) if x["high"] is not None and x["low"] is not None]
        return {"fetched": dt.datetime.now(tz).isoformat(timespec="minutes"), "days": out} if out else None
    except Exception as e:  # forecast is a bonus; never fail the build over it
        print("Forecast unavailable:", e)
        return None


def ics_escape(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics_fold(line):
    out, b = [], line.encode()
    while len(b) > 75:
        cut = 75 if not out else 74
        while cut and (b[cut] & 0xC0) == 0x80:  # don't split a UTF-8 character
            cut -= 1
        out.append(b[:cut].decode()); b = b[cut:]
    out.append(b.decode())
    return "\r\n ".join(out)


def build_ics(events, stamp):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//West Cajon Garden//Planting Calendar//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:West Cajon Garden",
             "X-WR-TIMEZONE:America/Los_Angeles", "X-WR-CALDESC:Planting and harvest windows from the West Cajon station's frost dates",
             "REFRESH-INTERVAL;VALUE=DURATION:PT12H", "X-PUBLISHED-TTL:PT12H"]
    for e in events:
        d = dt.date.fromisoformat(e["date"])
        lines += ["BEGIN:VEVENT", f"UID:{e['key']}@west-cajon-garden", f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}",
                  "SUMMARY:" + ics_escape(e["summary"].removeprefix("Garden: ") if hasattr(str, "removeprefix") else e["summary"].replace("Garden: ", "", 1)),
                  "DESCRIPTION:" + ics_escape(e["description"]), "TRANSP:TRANSPARENT", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(ics_fold(l) for l in lines) + "\r\n"


def render(data, crops):
    src = (HERE / "garden.src.html").read_text()
    out = src.replace("__STATION_DATA__", json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    return out.replace("__CROPS__", json.dumps(crops, ensure_ascii=False, separators=(",", ":")))


def render_offline():
    """Rebuild garden.html from the saved data/station.json, without fetching (used to republish the chat page)."""
    data = json.loads((HERE / "data" / "station.json").read_text())
    crops = json.loads((HERE / "crops.json").read_text())
    (HERE / "garden.html").write_text(render(data, crops))
    print("Built garden.html from saved station data of", data["updated"])


def main():
    dev = get(f"{BASE}/devices?public.slug={SLUG}")["data"][0]
    info = dev.get("info", {})
    ld = dev["lastData"]
    tz = ZoneInfo(ld.get("tz") or "America/Los_Angeles")
    mac = urllib.parse.quote(dev["macAddress"])
    time.sleep(1.2)
    start = int((time.time() - 420 * 86400) * 1000)
    days = get(f"{BASE}/device-data?macAddress={mac}&dataKey=deviceSummaries&start={start}&stats=summary")["data"]

    rows = []
    for r in days:
        d = dt.datetime.fromtimestamp(r["dateutc"] / 1000, tz).date()
        t = r.get("tempf") or {}
        if t.get("h") is None:
            continue
        sr, uv = r.get("solarradiation") or {}, r.get("uv") or {}
        rows.append({"d": d, "hi": t["h"], "lo": t["l"],
                     "rain": (r.get("dailyrainin") or {}).get("h") or 0,
                     "gust": (r.get("maxdailygust") or {}).get("h") or 0,
                     # sun: daily insolation in kWh/m2 (= peak sun hours) from per-minute W/m2; skip days with big gaps
                     "sun": round(sr["s"] / sr["c"] * 24 / 1000, 2) if (sr.get("c") or 0) >= 1200 else None,
                     "uv": uv.get("h"),
                     "uvAt": dt.datetime.fromtimestamp(uv["ht"] / 1000, tz).strftime("%H:%M") if uv.get("h") and uv.get("ht") else None})
    rows.sort(key=lambda x: x["d"])

    # frost dates: latest spring (Jan-Jun) and latest fall (Jul-Dec) frost seasons in the record
    frosts = [r for r in rows if r["lo"] <= 32]
    spring, fall = defaultdict(list), defaultdict(list)
    for r in frosts:
        (spring if r["d"].month < 7 else fall)[r["d"].year].append(r["d"])
    last_spring = max(spring[max(spring)]) if spring else None
    first_fall = min(fall[max(fall)]) if fall else None
    coldest = min(rows, key=lambda x: x["lo"]) if rows else None
    hottest = max(rows, key=lambda x: x["hi"]) if rows else None

    months = defaultdict(list)
    for r in rows:
        months[r["d"].strftime("%Y-%m")].append(r)
    mlist = []
    for ym in sorted(months)[-12:]:
        v = months[ym]
        sun = [x["sun"] for x in v if x["sun"] is not None]
        uvs = [x["uv"] for x in v if x["uv"] is not None]
        mlist.append({"ym": ym, "days": len(v),
                      "hi": round(sum(x["hi"] for x in v) / len(v), 1),
                      "lo": round(sum(x["lo"] for x in v) / len(v), 1),
                      "max": max(x["hi"] for x in v), "min": min(x["lo"] for x in v),
                      "rain": round(sum(x["rain"] for x in v), 2),
                      "frost": sum(1 for x in v if x["lo"] <= 32),
                      "gust": max(x["gust"] for x in v),
                      "sun": round(sum(sun) / len(sun), 2) if sun else None,
                      "uv": round(sum(uvs) / len(uvs), 1) if uvs else None,
                      "uvMax": max(uvs) if uvs else None})

    keep = ["tempf", "feelsLike", "humidity", "windspeedmph", "windgustmph", "maxdailygust", "winddir",
            "uv", "solarradiation", "hourlyrainin", "dailyrainin", "weeklyrainin", "monthlyrainin",
            "yearlyrainin", "baromrelin", "dateutc", "lastRain"]
    cur = {k: ld.get(k) for k in keep}
    hl = ld.get("hl") or {}
    cur["todayHi"] = (hl.get("tempf") or {}).get("h")
    cur["todayLo"] = (hl.get("tempf") or {}).get("l")
    hs, hu = hl.get("solarradiation") or {}, hl.get("uv") or {}
    cur["todaySun"] = round(hs["s"] / 60000, 2) if hs.get("s") is not None else None  # kWh/m2 so far (1-min samples)
    cur["todaySunPeak"] = hs.get("h")
    cur["todayUV"] = hu.get("h")
    cur["todayUVAt"] = dt.datetime.fromtimestamp(hu["ht"] / 1000, tz).strftime("%H:%M") if hu.get("h") and hu.get("ht") else None

    elev_m = (info.get("coords") or {}).get("elevation")

    data = {
        "links": {"claude": CLAUDE_URL, "site": SITE_URL, "ics": ICS_URL},
        "station": {"name": info.get("name", "Weather Station"),
                    "place": ((info.get("coords") or {}).get("location") or "Phelan") + ", CA",
                    "elevationFt": round(elev_m * 3.28084) if elev_m else None,
                    "dashboard": DASHBOARD},
        "updated": dt.datetime.now(tz).isoformat(timespec="minutes"),
        "current": cur,
        "forecast": nws_forecast(info, tz),
        "frost": {"lastSpring": last_spring.isoformat() if last_spring else None,
                  "firstFall": first_fall.isoformat() if first_fall else None,
                  "nights": len(frosts),
                  "coldest": {"d": coldest["d"].isoformat(), "t": coldest["lo"]} if coldest else None,
                  "hottest": {"d": hottest["d"].isoformat(), "t": hottest["hi"]} if hottest else None,
                  "recordStart": rows[0]["d"].isoformat() if rows else None},
        "months": mlist,
        "recent": [{"d": r["d"].isoformat(), "hi": r["hi"], "lo": r["lo"], "rain": r["rain"], "gust": r["gust"],
                    "sun": r["sun"], "uv": r["uv"], "uvAt": r["uvAt"]}
                   for r in rows[-14:]],
    }
    crops = json.loads((HERE / "crops.json").read_text())
    out = render(data, crops)
    today = dt.datetime.now(tz).date()
    events = calendar_events(crops, data["frost"], today)
    (HERE / "garden_events.json").write_text(json.dumps(
        {"generated": data["updated"], "timeZone": str(tz), "events": events}, indent=1))
    (HERE / "garden.html").write_text(out)
    (HERE / "data").mkdir(exist_ok=True)
    (HERE / "data" / "station.json").write_text(json.dumps(data, indent=1) + "\n")
    (HERE / "data" / "chat.html").write_text(out)  # republished to the claude.ai garden chat by a Claude routine
    site = HERE / "site"
    site.mkdir(exist_ok=True)
    (site / "index.html").write_text("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + out + "\n</html>\n")
    year_events = calendar_events(crops, data["frost"], today, horizon_days=365, lookback_days=30)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (site / "garden.ics").write_bytes(build_ics(year_events, stamp).encode())
    print("Built garden.html  | last spring frost", data["frost"]["lastSpring"], "| first fall frost",
          data["frost"]["firstFall"], "| temp", cur["tempf"], "|", len(events), "calendar events in next 6 weeks |", len(year_events), "in the calendar feed")


if __name__ == "__main__":
    import sys
    render_offline() if "--offline" in sys.argv else main()
