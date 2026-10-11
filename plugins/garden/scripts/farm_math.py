#!/usr/bin/env python3
"""Water and money arithmetic for the West Cajon farm.

  farm_math.py haul GALLONS [--price 60]            cost of hauling water ($ per 1,000 gal)
  farm_math.py roof SQFT INCHES [--eff 0.85]        gallons caught by a roof
  farm_math.py land ACRES INCHES [--k 0.3]          gallons running off land (k = runoff coefficient)
  farm_math.py cca CWR_MM DR_MM [--k 0.3] [--eff 0.6] [--basin-m2 AREA]
                                                    microcatchment catchment : cultivated area ratio
  farm_math.py return NET_DOLLARS GALLONS [--hours H] [--price 60]
                                                    net $ per 1,000 gal (and per hour) vs hauled water
"""
import argparse, sys

HAULED = 60.0          # $ per 1,000 gal delivered
ROOF_GAL = 623.0       # gal per inch per 1,000 sq ft
ACRE_GAL = 27154.0     # gal per inch per acre
AF_GAL = 325851.0      # gal per acre-foot


def haul(a):
    cost = a.gallons / 1000 * a.price
    print(f"{a.gallons:,.0f} gal hauled at ${a.price:,.0f}/1,000 gal = ${cost:,.0f}")
    print(f"({a.gallons / AF_GAL:.2f} acre-feet; Minimal Producer limit is 10 AF/yr)")


def roof(a):
    gal = a.sqft / 1000 * ROOF_GAL * a.inches * a.eff
    print(f"{a.inches} in on {a.sqft:,.0f} sq ft at {a.eff:.0%} collection = {gal:,.0f} gal "
          f"(worth ${gal / 1000 * HAULED:,.0f} at hauled prices)")


def land(a):
    gal = a.acres * ACRE_GAL * a.inches * a.k
    print(f"{a.inches} in on {a.acres} ac with runoff coefficient {a.k} = {gal:,.0f} gal of runoff")


def cca(a):
    if a.dr <= 0 or a.k <= 0 or a.eff <= 0:
        sys.exit("cca: rainfall, k and eff must be above zero")
    if a.cwr <= a.dr:
        print(f"Rain ({a.dr} mm) already meets the crop need ({a.cwr} mm): no extra catchment needed.")
        return
    ratio = (a.cwr - a.dr) / (a.dr * a.k * a.eff)
    print(f"C:CA = ({a.cwr} - {a.dr}) / ({a.dr} x {a.k} x {a.eff}) = {ratio:.1f} : 1")
    if a.basin_m2:
        print(f"A {a.basin_m2} m² basin needs {ratio * a.basin_m2:,.1f} m² of catchment, or drip for the shortfall.")


def ret(a):
    per = a.net / (a.gallons / 1000)
    print(f"${a.net:,.0f} net on {a.gallons:,.0f} gal = ${per:,.0f} per 1,000 gal")
    if a.hours:
        print(f"${a.net / a.hours:,.0f} per labour hour over {a.hours:,.0f} h")
    verdict = "beats" if per > a.price else "does not cover"
    print(f"That {verdict} hauled water at ${a.price:,.0f}/1,000 gal.")


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("haul"); s.add_argument("gallons", type=float)
    s.add_argument("--price", type=float, default=HAULED); s.set_defaults(fn=haul)

    s = sub.add_parser("roof"); s.add_argument("sqft", type=float); s.add_argument("inches", type=float)
    s.add_argument("--eff", type=float, default=0.85); s.set_defaults(fn=roof)

    s = sub.add_parser("land"); s.add_argument("acres", type=float); s.add_argument("inches", type=float)
    s.add_argument("--k", type=float, default=0.3); s.set_defaults(fn=land)

    s = sub.add_parser("cca"); s.add_argument("cwr", type=float); s.add_argument("dr", type=float)
    s.add_argument("--k", type=float, default=0.3); s.add_argument("--eff", type=float, default=0.6)
    s.add_argument("--basin-m2", type=float); s.set_defaults(fn=cca)

    s = sub.add_parser("return"); s.add_argument("net", type=float); s.add_argument("gallons", type=float)
    s.add_argument("--hours", type=float); s.add_argument("--price", type=float, default=HAULED)
    s.set_defaults(fn=ret)

    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main(sys.argv[1:])
