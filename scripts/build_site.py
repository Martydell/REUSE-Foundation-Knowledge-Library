#!/usr/bin/env python3
"""Builds docs/ as a static GitHub Pages site from organisations/*.md and data/REUSE_V4_Master.csv.
Free to re-run — no API calls needed, matching the project's CSV-generation cost philosophy."""

import csv
import html
import os
import re
import shutil

import markdown

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG_DIR = os.path.join(REPO_ROOT, "organisations")
CSV_PATH = os.path.join(REPO_ROOT, "data", "REUSE_V4_Master.csv")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
PROFILES_DIR = os.path.join(DOCS_DIR, "organisations")

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — REUSE Foundation Knowledge Library</title>
<meta name="description" content="{description}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>♻️</text></svg>">
<link rel="stylesheet" href="{css_path}">
</head>
<body>
<header class="site-header">
  <a class="brand" href="{home_path}">♻️ REUSE Foundation Knowledge Library</a>
</header>
<main class="profile">
{body}
</main>
<footer class="site-footer">
  <p>Research-grade circular-economy organisation database. <a href="{home_path}">Back to index</a></p>
</footer>
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>REUSE Foundation Knowledge Library</title>
<meta name="description" content="A research-grade, citable database of {count} circular-economy and reuse organisations worldwide.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>♻️</text></svg>">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
  <span class="brand">♻️ REUSE Foundation Knowledge Library</span>
</header>
<main class="index">
  <h1>{count} circular-economy &amp; reuse organisations</h1>
  <p class="subtitle">A research-grade, publicly-citable database of reuse, refill, deposit-return, and packaging-as-a-service organisations worldwide. Full methodology in the <a href="https://github.com/{gh_repo}">GitHub repo</a>.</p>

  <div class="controls">
    <input type="search" id="search" placeholder="Search by name, country, category…" autocomplete="off">
    <select id="country-filter"><option value="">All countries</option></select>
    <select id="priority-filter"><option value="">All priority ratings</option></select>
    <span id="result-count" class="result-count"></span>
  </div>

  <div class="table-wrap">
    <table id="org-table">
      <thead>
        <tr>
          <th data-key="name" class="sortable">Organisation</th>
          <th data-key="country" class="sortable">Country</th>
          <th data-key="categories">Categories</th>
          <th data-key="priority" class="sortable">Priority</th>
        </tr>
      </thead>
      <tbody id="org-table-body"></tbody>
    </table>
  </div>
</main>
<footer class="site-footer">
  <p>Data generated from <a href="data/REUSE_V4_Master.csv">REUSE_V4_Master.csv</a>. Last built: {build_date}.</p>
</footer>
<script src="assets/data.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""

CSS = """
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1a1f1a;
  --muted: #5b645b;
  --border: #d8ddd6;
  --accent: #1f7a4d;
  --accent-bg: #eaf5ee;
  --row-hover: #f4f8f4;
  --header-bg: #10331f;
  --header-fg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #12160f;
    --fg: #e9ede8;
    --muted: #a3ac9f;
    --border: #2c342a;
    --accent: #6fcf97;
    --accent-bg: #1a2b20;
    --row-hover: #1c231a;
    --header-bg: #0a1f13;
    --header-fg: #ffffff;
  }
}
:root[data-theme="dark"] {
  --bg: #12160f; --fg: #e9ede8; --muted: #a3ac9f; --border: #2c342a;
  --accent: #6fcf97; --accent-bg: #1a2b20; --row-hover: #1c231a;
  --header-bg: #0a1f13; --header-fg: #ffffff;
}
:root[data-theme="light"] {
  --bg: #ffffff; --fg: #1a1f1a; --muted: #5b645b; --border: #d8ddd6;
  --accent: #1f7a4d; --accent-bg: #eaf5ee; --row-hover: #f4f8f4;
  --header-bg: #10331f; --header-fg: #ffffff;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.55;
}
.site-header {
  background: var(--header-bg);
  color: var(--header-fg);
  padding: 1rem 1.5rem;
}
.site-header .brand {
  color: var(--header-fg);
  text-decoration: none;
  font-weight: 700;
  font-size: 1.1rem;
}
main.index, main.profile {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}
h1 { font-size: 1.6rem; margin-bottom: 0.4rem; }
.subtitle { color: var(--muted); max-width: 70ch; }
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
  margin: 1.4rem 0 1rem;
}
#search {
  flex: 1 1 260px;
  padding: 0.55rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg);
  color: var(--fg);
  font-size: 0.95rem;
}
select {
  padding: 0.55rem 0.6rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg);
  color: var(--fg);
  font-size: 0.9rem;
}
.result-count { color: var(--muted); font-size: 0.85rem; margin-left: auto; white-space: nowrap; }
.table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 10px; }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; }
thead th {
  text-align: left;
  padding: 0.65rem 0.8rem;
  background: var(--accent-bg);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  position: sticky; top: 0;
}
th.sortable { cursor: pointer; user-select: none; }
th.sortable:hover { color: var(--accent); }
tbody td { padding: 0.55rem 0.8rem; border-bottom: 1px solid var(--border); vertical-align: top; }
tbody tr:hover { background: var(--row-hover); }
tbody a { color: var(--accent); text-decoration: none; font-weight: 600; }
tbody a:hover { text-decoration: underline; }
.tag-pill {
  display: inline-block;
  font-size: 0.75rem;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  background: var(--accent-bg);
  color: var(--accent);
  margin: 0 0.25rem 0.25rem 0;
  white-space: nowrap;
}
.priority { font-size: 0.85rem; white-space: nowrap; }
main.profile h1 { font-size: 1.5rem; }
main.profile table { width: 100%; margin: 1rem 0; }
main.profile table th, main.profile table td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.7rem;
  text-align: left;
}
main.profile table th { background: var(--accent-bg); }
main.profile h2 { font-size: 1.1rem; margin-top: 1.8rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
main.profile a { color: var(--accent); }
.site-footer { text-align: center; color: var(--muted); font-size: 0.85rem; padding: 2rem 1.5rem 3rem; }
.site-footer a { color: var(--accent); }
@media (max-width: 640px) {
  .result-count { margin-left: 0; }
}
"""

SITE_JS = """
const state = { sortKey: 'name', sortDir: 1 };

function uniqueSorted(values) {
  return Array.from(new Set(values.filter(Boolean))).sort();
}

function populateFilters() {
  const countrySel = document.getElementById('country-filter');
  const prioritySel = document.getElementById('priority-filter');
  uniqueSorted(ORGS.map(o => o.country)).forEach(c => {
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = c;
    countrySel.appendChild(opt);
  });
  uniqueSorted(ORGS.map(o => o.priority)).forEach(p => {
    const opt = document.createElement('option');
    opt.value = p; opt.textContent = p;
    prioritySel.appendChild(opt);
  });
}

function matches(org, q, country, priority) {
  if (country && org.country !== country) return false;
  if (priority && org.priority !== priority) return false;
  if (!q) return true;
  const hay = (org.name + ' ' + org.country + ' ' + org.categories + ' ' + org.summary).toLowerCase();
  return hay.includes(q);
}

function render() {
  const q = document.getElementById('search').value.trim().toLowerCase();
  const country = document.getElementById('country-filter').value;
  const priority = document.getElementById('priority-filter').value;
  let rows = ORGS.filter(o => matches(o, q, country, priority));

  rows.sort((a, b) => {
    const av = (a[state.sortKey] || '').toString().toLowerCase();
    const bv = (b[state.sortKey] || '').toString().toLowerCase();
    if (av < bv) return -1 * state.sortDir;
    if (av > bv) return 1 * state.sortDir;
    return 0;
  });

  const tbody = document.getElementById('org-table-body');
  tbody.innerHTML = rows.map(o => `
    <tr>
      <td><a href="organisations/${o.slug}.html">${o.name}</a></td>
      <td>${o.country || '—'}</td>
      <td>${(o.categories || '').split(',').filter(Boolean).map(t => `<span class="tag-pill">${t.trim()}</span>`).join('')}</td>
      <td class="priority">${o.priority || '—'}</td>
    </tr>
  `).join('');

  document.getElementById('result-count').textContent = `${rows.length} of ${ORGS.length} organisations`;
}

document.getElementById('search').addEventListener('input', render);
document.getElementById('country-filter').addEventListener('change', render);
document.getElementById('priority-filter').addEventListener('change', render);

document.querySelectorAll('th.sortable').forEach(th => {
  th.addEventListener('click', () => {
    const key = th.dataset.key;
    if (state.sortKey === key) { state.sortDir *= -1; } else { state.sortKey = key; state.sortDir = 1; }
    render();
  });
});

populateFilters();
render();
"""


def slugify_fallback(name):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip()).strip("-").lower()
    return s


def load_rows():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def convert_org_md_to_html(slug, name):
    md_path = os.path.join(ORG_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        return None
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    body_html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return body_html


def build_profile_pages(rows):
    os.makedirs(PROFILES_DIR, exist_ok=True)
    written = 0
    for row in rows:
        slug = row.get("GitHub slug", "").strip()
        name = row.get("Organisation", "").strip()
        if not slug:
            slug = slugify_fallback(name)
        body_html = convert_org_md_to_html(slug, name)
        if body_html is None:
            continue
        summary = row.get("Short summary", "").strip() or f"Profile of {name}, a circular-economy organisation."
        description = html.escape(summary[:280])
        page = PAGE_TEMPLATE.format(
            title=html.escape(name),
            description=description,
            css_path="../assets/style.css",
            home_path="../index.html",
            body=body_html,
        )
        out_path = os.path.join(PROFILES_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)
        written += 1
    return written


def build_index(rows):
    orgs_js = []
    for row in rows:
        slug = row.get("GitHub slug", "").strip() or slugify_fallback(row.get("Organisation", ""))
        orgs_js.append({
            "name": row.get("Organisation", "").strip(),
            "slug": slug,
            "country": row.get("Country", "").strip(),
            "categories": row.get("Tags", "").strip() or row.get("Categories", "").strip(),
            "priority": row.get("REUSE priority rating", "").strip(),
            "summary": row.get("Short summary", "").strip(),
        })

    import json
    data_js = "const ORGS = " + json.dumps(orgs_js, ensure_ascii=False) + ";\n"

    assets_dir = os.path.join(DOCS_DIR, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(assets_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(assets_dir, "site.js"), "w", encoding="utf-8") as f:
        f.write(SITE_JS)
    with open(os.path.join(assets_dir, "data.js"), "w", encoding="utf-8") as f:
        f.write(data_js)

    import datetime
    build_date = datetime.date.today().isoformat()
    index_html = INDEX_TEMPLATE.format(
        count=len(rows),
        gh_repo="Martydell/REUSE-Foundation-Knowledge-Library",
        build_date=build_date,
    )
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)


def main():
    rows = load_rows()
    os.makedirs(DOCS_DIR, exist_ok=True)
    # Copy CSV for direct download/browse
    shutil.copyfile(CSV_PATH, os.path.join(DOCS_DIR, "REUSE_V4_Master.csv"))
    # .nojekyll so GitHub Pages serves files as-is (avoids Jekyll processing conflicts)
    with open(os.path.join(DOCS_DIR, ".nojekyll"), "w") as f:
        f.write("")
    written = build_profile_pages(rows)
    build_index(rows)
    print(f"Wrote {written} profile pages + index.html to docs/ (from {len(rows)} CSV rows)")


if __name__ == "__main__":
    main()
