# Estonian Probability Scale

A small data pipeline that pulls a curated set of Estonian government
statistics, computes conditional probabilities (shares) from them, and
renders them on a single non-linear horizontal scale -- so a reader can
see how 0.0076 ("cannabinoids share of F10-F19 disorders") and 0.6586
("alcohol share of F10-F19 disorders") sit relative to each other on a
0-1 axis.

Submitted as the RMK 2026 data team internship test challenge. The
challenge brief is at
<https://github.com/rmk-internship/2026/blob/main/test/test_challenge.md>.

## Data sources

Data is fetched at runtime via the public JSON-STAT2 APIs of:

- **Statistics Estonia** -- `andmed.stat.ee/api/v1/et/stat`
  (datasets `KA10`, `KA30`, `PM09`, `RV262`, `RV271`, `TS093`)
- **National Institute for Health Development (TAI)** --
  `statistika.tai.ee/api/v1/et/Andmebaas`
  (datasets `PKH7`, `VIG10`, `KE32`)

Neither API requires authentication. The exact query payloads (filtered
to the dimensions actually used) live inline in
`src/data_process/retrieve_data.py`.

> Note: this project is *for* the RMK internship, but RMK
> (Riigimetsa Majandamise Keskus) does not host these APIs -- the data
> comes from Statistics Estonia and TAI.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

`main.py`:

1. Pulls the 9 datasets from the APIs and writes them as standardised
   CSVs to `./output/`.
2. Computes the 14 probabilities listed below.
3. Saves the chart to `./images/probabilities_horizontal_scale.png`.

Both `output/` and `images/` are gitignored; running the pipeline
regenerates them.

## What is computed

| # | Label                                              | What the denominator is                          |
|---|----------------------------------------------------|--------------------------------------------------|
| 1 | Shrimp share of EE ocean catch                     | All-species ocean catch, kg, all years           |
| 2 | Sardine share of EE ocean catch                    | All-species ocean catch, kg, all years           |
| 3 | Perch share of L. Peipsi catch                     | Lake Peipsi catch, kg, all years                 |
| 4 | Pike share of L. Peipsi catch                      | Lake Peipsi catch, kg, all years                 |
| 5 | Cannabinoids share of F10-F19 cases                | Psychoactive substance disorder cases (F10-F19)  |
| 6 | Alcohol share of F10-F19 cases                     | Psychoactive substance disorder cases (F10-F19)  |
| 7 | July share of all EE marriages                     | All marriages, all years (peak month)            |
| 8 | January share of all EE marriages                  | All marriages, all years (lowest month)          |
| 9 | Age 25-29 share of EE marriages                    | All marriages, all years (peak age band)         |
| 10| Drunk-driver share of EE road accidents            | All road accidents, all years                    |
| 11| August share of yearly road accidents              | All road accidents, all years (peak month)       |
| 12| Pedestrian share of vehicle-accident injuries      | Vehicle-accident injuries, V01-V99               |
| 13| Cyclist share of vehicle-accident injuries         | Vehicle-accident injuries, V01-V99               |
| 14| Ambulance share of EE ER arrivals                  | All emergency-medical patients                   |

## Methodology and caveats

A few things a reviewer should know up front:

- **These are not lifetime event probabilities.** The challenge brief
  motivates the scale with examples like "P(throwing 4 heads in a row) =
  0.06". Most public Estonian data is *categorical* rather than
  *event-frequency*, so what's plotted here is conditional shares -- "of
  all road accidents in EE, fraction involving an intoxicated driver",
  not "if you drive in EE today, what's P(accident)". The labels are
  written as "X share of Y" specifically to keep that distinction
  obvious.

- **Aggregation is across all years in each dataset**, not
  per-year-then-averaged. The denominator is the absolute total for the
  fetched window. This is the simplest unbiased estimate; it ignores
  inter-year variation, which is fine for an intuition-building scale.

- **PM09 (livestock counts) was deliberately excluded.** That dataset
  mixes leaf categories ("Piimauted") with hierarchical aggregates
  ("Lambad", "Sead", "Veised"), so naively dividing each `Liik` row by
  the sum across all `Liik` rows double-counts and produces a
  meaningless near-zero result. Fixing this properly needs the PM09
  taxonomy metadata, which would be a follow-up.

- **A pie chart was deliberately not produced.** The 14 values come
  from 9 unrelated datasets with no common denominator, so showing them
  as slices of a single whole would imply a relationship that isn't
  there.

- **The horizontal scale uses a sqrt transform** (more resolution at
  low p, less at high p). This is debatable for a probability scale --
  a log axis would be more standard -- but at the magnitudes seen here
  (~0.01 .. 0.66) the sqrt stretch gives readable separation at the
  low end without compressing the high end into the right wall.

## What I'd do with more time

Bullet-list of things knowingly skipped, in rough priority order. The
challenge brief explicitly invites describing the proposed-but-not-built
parts of the solution.

- **Switch to a log-base-10 axis** with grid lines at 10^-3, 10^-2,
  10^-1, 1, and add reference points from the brief's example image
  ("0.0019 = born with 11 fingers", "0.06 = four heads in a row") so
  domain-conditional shares can be visually compared against intuitive
  lifetime probabilities.
- **Add genuine event-frequency probabilities**, e.g. P(snow before
  October 1 in Tallinn | year) from Estonian weather records, P(any
  given EE driver in an accident in a year) by joining accident counts
  with the licensed-driver census. These would belong on the scale next
  to the conditional shares with a different marker shape.
- **Bayesian update example**: take one of the conditional shares,
  e.g. "P(disorder is alcohol | psychoactive-substance disorder)", and
  compute the unconditional P(alcohol disorder | adult EE resident)
  using TAI prevalence data, demonstrating P(B|A) -> P(A|B) explicitly.
- **Move the inline query payloads** out of `retrieve_data.py` and into
  one JSON file per dataset under `data/queries/`. The current 580-line
  file is mostly literal JSON.
- **Resolve the PM09 hierarchy** so the livestock entry can be added
  correctly.

## Project structure

```
.
├── main.py                              # Pipeline entry point
├── requirements.txt
├── LICENSE
├── README.md
└── src/
    ├── API/
    │   ├── api_client.py                # HTTP client w/ retry & rate-limit
    │   └── data_validator.py            # JSON-STAT -> DataFrame conversion
    ├── data_process/
    │   ├── data_request.py              # Multi-dataset orchestrator
    │   ├── csv_converter.py             # DataFrame -> standardised CSV
    │   └── retrieve_data.py             # Query payloads + pipeline glue
    └── prob_extraction/
        └── extract_probabilities.py     # Probabilities + horizontal scale
```

`output/` (raw CSVs) and `images/` (rendered chart) are created by
`main.py` and are gitignored.

## License

MIT. See `LICENSE`.
