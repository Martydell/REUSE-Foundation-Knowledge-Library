# REUSE Foundation brand assets

- `reuse-foundation-icon.png` — the official REUSE Foundation logo mark, sourced from
  [reusefoundation.org](https://www.reusefoundation.org) (cropped to its content bounding box;
  no other edits). A smaller web-sized copy lives at `docs/assets/reuse-logo.png` for the site,
  and is also embedded as a base64 data URI in `analysis/feature_analysis_report.html` so that
  report stays a single self-contained file.

## Brand colors

Sourced directly from the live site and the logo's own pixel values:

| Token | Hex | Usage |
|---|---|---|
| Signature blue | `#57c7ff` | Logo, decorative accents, dark-mode text/links (passes contrast on black) |
| Deepened blue | `#006699` | Light-mode text/links — the signature blue alone fails WCAG contrast on white (1.9:1) |
| Black | `#000000` | Primary background (their site is black-first, not just "dark mode") |
| White | `#ffffff` | Primary background (light mode) |
| Body ink | `#282626` | Body text on white, per the live site's own inline styles |

Both `scripts/build_site.py` and `scripts/render_feature_analysis_html.py` define these as CSS
custom properties (`--accent`, `--accent-bright`/`--accent-dark`, etc.) rather than hard-coding
the hex values inline — update them there if the real brand ever changes.
