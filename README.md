# REUSE Foundation Knowledge Library (V4)

Research-grade organisational profiles for the REUSE Foundation Master List — 748 circular economy, reuse, and refill organisations.

This is **version 2** of the REUSE Foundation library, built to the V4 research standard (verified sources, confidence ratings, GitHub-ready markdown profiles). The original spreadsheet-only version remains live at [martydell.github.io/Reuse-foundation-library](https://martydell.github.io/Reuse-foundation-library/) as v1.

## Structure

- `data/REUSE_Master_List.csv` — working master dataset (748 rows), updated as each organisation is researched to V4 depth.
- `data/source/` — original source spreadsheets and the V4 output format example.
- `organisations/` — one markdown profile per organisation (Section T output of the V4 prompt), filename = slugified org name.
- `PROGRESS.md` — tracks research status per organisation.

## Methodology

Each organisation is researched using the REUSE Foundation Master Library Research Prompt (Version 4): verified public sources only (official sites, annual/impact/sustainability reports, government/company registries, academic and NGO publications), with explicit confidence ratings (High/Medium/Low) for name, founding year, and impact data. Unverifiable fields are marked "Not publicly available" rather than estimated. See `data/source/V4_format_example_20_orgs.csv` for the target field format.
