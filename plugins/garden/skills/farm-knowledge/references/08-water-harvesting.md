# Dryland water harvesting, earthworks and ponds

Design manuals kept in the owner's project files: ICARDA *Rainwater Harvesting Design Manual: Micro-catchment
Systems for Drylands Agriculture* (Oweis & Haddad, 2024); NRCS Ag Handbook 590 *Ponds*; K.D. Nelson *Design and
Construction of Small Earth Dams* (1985); OSU *Woodland Ponds*. Free: Lancaster's *Eight Rainwater Harvesting
Principles*; Quivira Coalition / Zeedyk *Erosion Control Field Guide*.

## Brad Lancaster's eight principles
1. Begin with long and thoughtful observation.
2. Start at the top (highpoint) of your watershed and work down.
3. Start small and simple.
4. Spread and infiltrate the flow of water.
5. Always plan an overflow route, and manage overflow as a resource.
6. Maximise living, organic groundcover.
7. Maximise beneficial relationships and efficiency by stacking functions.
8. Continually reassess your system.
Watershed Management Group shorthand: **slow it, spread it, sink it, (store it)**.

## Useful numbers
- **Roof yield:** 1 in on 1,000 sq ft = 623 gal (x 0.8-0.9 collection efficiency; the plan uses 85%).
- **Land yield:** 1 in on 1 acre = 27,154 gal. 1 acre-foot = 325,851 gal.
- **Runoff coefficients:** roofs 0.8-0.95; compacted dirt road 0.3-0.6; bare desert soil 0.1-0.5 depending on crust
  and intensity; vegetated 0.05-0.2. Crusts shed a lot in intense storms and almost nothing in gentle ones.
- **Evaporation:** open water in the high desert loses on the order of 6+ ft (~2 m) a year. The plan's own pond
  estimate was ~780 m³/yr evaporation from a 376 m³ pond. Covered tanks, deep narrow ponds, floating covers or shade
  balls, and storage in the soil profile beat open water.
- **Peak intensity on site:** 1.3 in/hr recorded; size gutters and downspouts for it.

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/farm_math.py"` computes roof and land yield, hauled-water cost and C:CA.

## Microcatchment sizing (FAO, Critchley & Siegert 1991; ICARDA)

C : CA = (CWR − DR) / (DR × K × Eff)

- CWR = seasonal crop water requirement (mm); DR = design rainfall (mm, use a dry-year value, e.g. 67% exceedance);
  K = runoff coefficient of the catchment; Eff = efficiency of use (0.5-0.75).
- Dry-year example: mature jujube needing ~500 mm over its root area, DR = 150 mm, K = 0.3, Eff = 0.6 →
  (500-150)/(150 x 0.3 x 0.6) ≈ 13:1. Each basin needs ~13x its root area of catchment, or drip.
- Average-year example: DR = 250 mm, K = 0.4, Eff = 0.6 → ≈ 4:1.
- This is why trees here are either drip-supplemented or widely spaced with large catchments.
- ICARDA types: **negarim** (diamond basins for trees), contour ridges/bunds, **half-moons**, **zaï pits**, Vallerani
  machine pits.

## Earthworks toolkit
| Structure | Where | Notes |
|---|---|---|
| Basins (sunken planting basins) | Each tree, downspouts | Cheapest, most robust in sand; mulch-filled |
| Half-moon / boomerang berms | Slopes 1-5%, single trees or shrubs | Open side uphill; overflow around the tips |
| Swales | Gentle slopes, deep soil | Doherty: largely redundant with KPC; level spillways always; avoid on dispersive soils |
| Keyline pattern cultivation | Cover-cropped alleys | ~$0.02/m² (Doherty), temporary |
| Contour/keyline berms with trees | Main tree rows | Plan grades 0.4% to N with end basins |
| Infiltration basins / recharge pits | Below roads, lanes, roofs | Plan's north-side basins (82 m³) |
| Check dams (loose rock) | Lanes, small rills | 0.3-0.4 m high; toe of one level with the crest of the next |
| One rock dam (Zeedyk) | Small gullies | One rock high; traps sediment and seed |
| Zuni bowl (Zeedyk) | Headcuts | Rock-lined plunge pool that stops headcut migration |
| Media luna (Zeedyk) | Sheet flow onto bare ground | Crescent of rock that spreads flow |
| Rock rundown | Short steep drops | Armoured ramp |
| Baffles / induced meandering | Incised channels | *Let the Water Do the Work* (Zeedyk & Clothier, 2009) |
| Gabions | Larger washes | Engineering and possibly permits |
| Off-channel basin with take-off sill | Beside the wash | Silt trap, armoured overflow; permit first |
| Sand / subsurface dams | Sandy seasonal beds | Store water in sand with almost no evaporation; permits required |
| Waffle gardens / sunken beds | Annual vegetables | Zuni technique; collect water, cut wind |

## Low-tech, process-based restoration (the wash)
Utah State *Low-Tech Process-Based Restoration of Riverscapes Design Manual* (free); Zeedyk / Quivira erosion
control guides; Craig Sponholtz (Dryland Solutions).

## Ponds and dams
- NRCS AH-590 and Nelson: site selection, soils (≥20% clay or a liner), embankments (3:1 upstream, 2:1 downstream
  typical), spillway sizing for the design storm, cut-off trench, compaction in 6-8 in lifts.
- Sealing sand: bentonite, compacted clay, or geomembrane. Gley is unreliable in coarse sand.
- **The owner's decision:** the pond is an unlined recharge and habitat basin, so sealing is not needed; water to be
  pumped later goes in covered tanks.
- Permits: county grading permit; CDFW §1602 agreement for work in or diverting from a streambed; Division of Safety
  of Dams only for very large dams (not likely here).

## Roof water and tanks
- The California Rainwater Capture Act (2012) allows rooftop capture without a water right; check county rules for
  tank size, foundations and overflow.
- First-flush diverter, leaf screen, sealed opaque tanks, overflow to a basin away from foundations, insulate or bury
  exposed pipe against freeze. Tanks cost about $0.80-1.50 per gallon installed.

## Greywater
- California Plumbing Code Ch. 15: a laundry-to-landscape system needs no permit if it meets the code (no storage,
  subsurface or mulch-basin discharge, labelled, 3-way valve to sewer/septic). Simple and complex systems need
  permits. Art Ludwig *Create an Oasis with Greywater*; Greywater Action.
- On a septic parcel, also check the county's onsite wastewater rules.

## Irrigation efficiency
- Pressure-compensating drip; ollas for beds; deep pipes for trees; water at night or early morning; mulch.
- Gravity drip works from ~3-5 m of head; most drip needs 10-25 psi (7-17 m), so plan a header tank or a small solar
  pump. One 400 W panel and a small DC pump can lift the plan's annual demand.

## How it applies here
- The plan's water system (roof tanks, off-channel basin, row basins, lane check dams) follows these principles.
- Check every tree basin with C:CA; anything its catchment can't supply needs drip from tanks or the well.
- Water-harvesting design and installation for neighbouring desert properties is a real service business once the
  site is a working demonstration (`10-business.md`).
