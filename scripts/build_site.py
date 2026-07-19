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
  <div class="brand-block">
    <span class="brand">♻️ REUSE Foundation Knowledge Library</span>
    <p class="tagline">{count} circular-economy &amp; reuse organisations, researched and sourced worldwide.</p>
  </div>
</header>
<main class="index">
  <p class="subtitle">A research-grade, publicly-citable database of reuse, refill, deposit-return, and packaging-as-a-service organisations worldwide. Full methodology in the <a href="https://github.com/{gh_repo}">GitHub repo</a>.</p>

  <div id="summary" class="summary"></div>

  <div class="panel">
    <div class="controls">
      <div class="control">
        <label for="search">Search</label>
        <input type="search" id="search" placeholder="Name, country, category, summary…" autocomplete="off">
      </div>
      <div class="control">
        <label for="country-filter">Country</label>
        <select id="country-filter"><option value="">All countries</option></select>
      </div>
      <div class="control">
        <label for="priority-filter">Priority rating</label>
        <select id="priority-filter"><option value="">All ratings</option></select>
      </div>
      <div class="control">
        <label for="status-filter">Status</label>
        <select id="status-filter"><option value="">All statuses</option></select>
      </div>
    </div>
    <div class="actions">
      <div class="view-tabs">
        <button id="cardBtn" class="active" onclick="setView('cards')">Card view</button>
        <button id="tableBtn" onclick="setView('table')">Table view</button>
      </div>
      <button class="secondary" onclick="resetFilters()">Reset filters</button>
      <span id="result-count" class="result-count"></span>
    </div>
  </div>

  <div id="cards" class="cards"></div>

  <div id="tableWrap" class="table-wrap hidden">
    <table id="org-table">
      <thead>
        <tr>
          <th data-key="name" class="sortable">Organisation</th>
          <th data-key="country" class="sortable">Country</th>
          <th data-key="categories">Categories</th>
          <th data-key="year" class="sortable">Founded</th>
          <th data-key="status" class="sortable">Status</th>
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
  --bg: #f6f8f5;
  --card: #ffffff;
  --fg: #17312b;
  --muted: #63736e;
  --accent: #1e7d59;
  --accent-dark: #0f5d41;
  --accent-bg: #eef4f1;
  --teal: #e5f4ee;
  --amber: #fff2cc;
  --amber-fg: #735600;
  --red: #fde8e8;
  --red-fg: #9b1c1c;
  --border: #d8e2dc;
  --row-hover: #fbfdfb;
  --shadow: 0 8px 24px rgba(20,48,40,.08);
  --header-fg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0e1512;
    --card: #17211c;
    --fg: #e9ede8;
    --muted: #a3ac9f;
    --accent: #6fcf97;
    --accent-dark: #9be8bb;
    --accent-bg: #1a2b20;
    --teal: #16332a;
    --amber: #3a2f10;
    --amber-fg: #e8d290;
    --red: #3a1616;
    --red-fg: #f4a6a6;
    --border: #2c342a;
    --row-hover: #1c231a;
    --shadow: 0 8px 24px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"] {
  --bg: #0e1512; --card: #17211c; --fg: #e9ede8; --muted: #a3ac9f;
  --accent: #6fcf97; --accent-dark: #9be8bb; --accent-bg: #1a2b20;
  --teal: #16332a; --amber: #3a2f10; --amber-fg: #e8d290;
  --red: #3a1616; --red-fg: #f4a6a6; --border: #2c342a; --row-hover: #1c231a;
  --shadow: 0 8px 24px rgba(0,0,0,.35);
}
:root[data-theme="light"] {
  --bg: #f6f8f5; --card: #ffffff; --fg: #17312b; --muted: #63736e;
  --accent: #1e7d59; --accent-dark: #0f5d41; --accent-bg: #eef4f1;
  --teal: #e5f4ee; --amber: #fff2cc; --amber-fg: #735600;
  --red: #fde8e8; --red-fg: #9b1c1c; --border: #d8e2dc; --row-hover: #fbfdfb;
  --shadow: 0 8px 24px rgba(20,48,40,.08);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.55;
}
.site-header {
  padding: 2.1rem 2.2rem 1.7rem;
  background: linear-gradient(135deg, #12392d, #1e7d59);
  color: var(--header-fg);
}
.site-header .brand {
  color: var(--header-fg);
  text-decoration: none;
  font-weight: 800;
  font-size: 1.7rem;
  letter-spacing: -0.02em;
}
.site-header .tagline { margin: 0.4rem 0 0; max-width: 900px; color: #e6fff4; line-height: 1.5; }
main.index, main.profile {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 2rem 4rem;
}
h1 { font-size: 1.6rem; margin-bottom: 0.4rem; }
.subtitle { color: var(--muted); max-width: 80ch; margin: 1.2rem 0 1.2rem; }
.subtitle a, .site-footer a { color: var(--accent-dark); font-weight: 600; }
.summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1.2rem;
}
.metric {
  background: var(--card); border: 1px solid var(--border); box-shadow: var(--shadow);
  border-radius: 18px; padding: 1.1rem;
}
.metric .label { color: var(--muted); font-size: 0.8rem; }
.metric .value { font-size: 1.8rem; font-weight: 800; margin-top: 0.3rem; }
.panel {
  background: var(--card); border: 1px solid var(--border); box-shadow: var(--shadow);
  border-radius: 20px; padding: 1.1rem; margin-bottom: 1.1rem;
}
.controls {
  display: grid;
  grid-template-columns: 2fr repeat(3, 1fr);
  gap: 0.75rem;
  align-items: end;
}
.control label {
  display: block; font-size: 0.75rem; font-weight: 700; color: var(--muted);
  margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.03em;
}
#search, select {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--card);
  color: var(--fg);
  font-size: 0.9rem;
}
.actions { display: flex; align-items: center; gap: 0.6rem; margin-top: 0.9rem; flex-wrap: wrap; }
button {
  border: 0; border-radius: 999px; padding: 0.55rem 0.9rem; cursor: pointer;
  background: var(--accent); color: #fff; font-weight: 700; font-size: 0.85rem;
}
button.secondary, .view-tabs button { background: var(--accent-bg); color: var(--accent-dark); }
.view-tabs { display: flex; gap: 0.5rem; }
.view-tabs button.active { background: var(--accent); color: #fff; }
.result-count { color: var(--muted); font-size: 0.85rem; margin-left: auto; white-space: nowrap; }

.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
.card {
  background: var(--card); border: 1px solid var(--border); box-shadow: var(--shadow);
  border-radius: 20px; padding: 1.1rem; display: flex; flex-direction: column; gap: 0.7rem;
}
.card h2 { margin: 0; font-size: 1.15rem; letter-spacing: -0.01em; }
.card h2 a { color: var(--fg); text-decoration: none; }
.card h2 a:hover { color: var(--accent-dark); text-decoration: underline; }
.card .meta { display: flex; gap: 0.45rem; flex-wrap: wrap; }
.pill {
  display: inline-flex; align-items: center; border-radius: 999px;
  background: var(--accent-bg); padding: 0.25rem 0.55rem; font-size: 0.72rem;
  font-weight: 700; color: var(--accent-dark); white-space: nowrap;
}
.pill.score { background: var(--teal); }
.pill.warn { background: var(--amber); color: var(--amber-fg); }
.pill.bad { background: var(--red); color: var(--red-fg); }
.card .small { font-size: 0.82rem; color: var(--muted); line-height: 1.45; }
.card .field { border-top: 1px solid var(--border); padding-top: 0.55rem; }
.card .field strong {
  display: block; font-size: 0.7rem; color: var(--muted); text-transform: uppercase;
  letter-spacing: 0.04em; margin-bottom: 0.2rem;
}
.card .tags .tag-pill { margin: 0 0.25rem 0.25rem 0; }
.card .view-link { margin-top: auto; font-weight: 700; color: var(--accent-dark); text-decoration: none; font-size: 0.85rem; }
.card .view-link:hover { text-decoration: underline; }

.tag-pill {
  display: inline-block; font-size: 0.72rem; padding: 0.12rem 0.5rem; border-radius: 999px;
  background: var(--accent-bg); color: var(--accent-dark); margin: 0 0.25rem 0.25rem 0; white-space: nowrap;
}

.table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 18px; box-shadow: var(--shadow); }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; background: var(--card); }
thead th {
  text-align: left; padding: 0.7rem 0.8rem; background: #12392d; color: #fff;
  white-space: nowrap; position: sticky; top: 0;
}
th.sortable { cursor: pointer; user-select: none; }
tbody td { padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); vertical-align: top; }
tbody tr:hover td { background: var(--row-hover); }
tbody a { color: var(--accent-dark); text-decoration: none; font-weight: 600; }
tbody a:hover { text-decoration: underline; }
.priority { font-size: 0.85rem; white-space: nowrap; }
.hidden { display: none !important; }

main.profile h1 { font-size: 1.5rem; }
main.profile { max-width: 960px; }
main.profile table { width: 100%; margin: 1rem 0; background: var(--card); }
main.profile table th, main.profile table td {
  border: 1px solid var(--border); padding: 0.5rem 0.7rem; text-align: left;
}
main.profile table th { background: var(--accent-bg); }
main.profile h2 { font-size: 1.1rem; margin-top: 1.8rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
main.profile a { color: var(--accent-dark); }
.site-footer { text-align: center; color: var(--muted); font-size: 0.85rem; padding: 2rem 1.5rem 3rem; }

@media (max-width: 980px) {
  .site-header, main.index, main.profile { padding-left: 1.1rem; padding-right: 1.1rem; }
  .summary { grid-template-columns: repeat(2, 1fr); }
  .controls { grid-template-columns: 1fr; }
  .cards { grid-template-columns: 1fr; }
  table { min-width: 720px; }
}
"""

SITE_JS = """
const state = { sortKey: 'name', sortDir: 1, view: 'cards' };

function escapeHtml(str) {
  return String(str ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
}

function uniqueSorted(values) {
  return Array.from(new Set(values.filter(Boolean))).sort();
}

function populateFilters() {
  const countrySel = document.getElementById('country-filter');
  const prioritySel = document.getElementById('priority-filter');
  const statusSel = document.getElementById('status-filter');
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
  uniqueSorted(ORGS.map(o => o.status)).forEach(s => {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    statusSel.appendChild(opt);
  });
}

function matches(org, q, country, priority, status) {
  if (country && org.country !== country) return false;
  if (priority && org.priority !== priority) return false;
  if (status && org.status !== status) return false;
  if (!q) return true;
  const hay = (org.name + ' ' + org.country + ' ' + org.categories + ' ' + org.summary).toLowerCase();
  return hay.includes(q);
}

function getFiltered() {
  const q = document.getElementById('search').value.trim().toLowerCase();
  const country = document.getElementById('country-filter').value;
  const priority = document.getElementById('priority-filter').value;
  const status = document.getElementById('status-filter').value;
  let rows = ORGS.filter(o => matches(o, q, country, priority, status));
  rows.sort((a, b) => {
    const av = (a[state.sortKey] || '').toString().toLowerCase();
    const bv = (b[state.sortKey] || '').toString().toLowerCase();
    if (av < bv) return -1 * state.sortDir;
    if (av > bv) return 1 * state.sortDir;
    return 0;
  });
  return rows;
}

function priorityClass(priority) {
  const p = String(priority || '');
  if (p.includes('Essential') || p.includes('★★★★★')) return 'pill score';
  if (p.includes('High') || p.includes('★★★★')) return 'pill score';
  if (p.includes('Low relevance') || p.includes('★')) {
    if (p.includes('Low relevance')) return 'pill bad';
    if (p.includes('★★')) return 'pill warn';
  }
  return 'pill';
}

function statusClass(status) {
  const s = String(status || '').toLowerCase();
  if (s.includes('inactive') || s.includes('closed') || s.includes('defunct') || s.includes('ceased')) return 'pill bad';
  if (s.includes('uncertain') || s.includes('unclear') || s.includes('unverified')) return 'pill warn';
  return 'pill';
}

function renderSummary(rows) {
  const withHighPriority = rows.filter(o => /Essential|High/.test(o.priority || '')).length;
  const active = rows.filter(o => /active/i.test(o.status || '') && !/inactive/i.test(o.status || '')).length;
  const countries = new Set(rows.map(o => o.country).filter(c => c && c !== 'Not publicly available')).size;
  document.getElementById('summary').innerHTML = `
    <div class="metric"><div class="label">Organisations shown</div><div class="value">${rows.length}</div></div>
    <div class="metric"><div class="label">Essential / High priority</div><div class="value">${withHighPriority}</div></div>
    <div class="metric"><div class="label">Confirmed active</div><div class="value">${active}</div></div>
    <div class="metric"><div class="label">Countries represented</div><div class="value">${countries}</div></div>
  `;
}

function renderCards(rows) {
  document.getElementById('cards').innerHTML = rows.map(o => `
    <article class="card">
      <div>
        <h2><a href="organisations/${o.slug}.html">${escapeHtml(o.name)}</a></h2>
        <div class="meta">
          <span class="${priorityClass(o.priority)}">${escapeHtml(o.priority || 'Not rated')}</span>
          <span class="${statusClass(o.status)}">${escapeHtml(o.status || 'Status unknown')}</span>
        </div>
      </div>
      <div class="small"><strong>${escapeHtml(o.country || 'Country unknown')}</strong>${o.year ? ' · ' + (/found/i.test(o.year) ? '' : 'Founded ') + escapeHtml(o.year) : ''}</div>
      <div class="field">
        <strong>Overview</strong>
        <span class="small">${escapeHtml(o.summary || 'Not publicly available')}</span>
      </div>
      <div class="field tags">
        <strong>Categories</strong>
        ${(o.categories || '').split(',').filter(Boolean).map(t => `<span class="tag-pill">${escapeHtml(t.trim())}</span>`).join('') || '<span class="small">Not publicly available</span>'}
      </div>
      <a class="view-link" href="organisations/${o.slug}.html">View full profile →</a>
    </article>
  `).join('');
}

function renderTable(rows) {
  const tbody = document.getElementById('org-table-body');
  tbody.innerHTML = rows.map(o => `
    <tr>
      <td><a href="organisations/${o.slug}.html">${escapeHtml(o.name)}</a></td>
      <td>${escapeHtml(o.country) || '—'}</td>
      <td>${(o.categories || '').split(',').filter(Boolean).map(t => `<span class="tag-pill">${escapeHtml(t.trim())}</span>`).join('')}</td>
      <td>${escapeHtml(o.year) || '—'}</td>
      <td><span class="${statusClass(o.status)}">${escapeHtml(o.status || '—')}</span></td>
      <td class="priority">${escapeHtml(o.priority) || '—'}</td>
    </tr>
  `).join('');
}

function render() {
  const rows = getFiltered();
  document.getElementById('result-count').textContent = `Showing ${rows.length} of ${ORGS.length} organisations`;
  renderSummary(rows);
  if (state.view === 'cards') renderCards(rows); else renderTable(rows);
}

function setView(view) {
  state.view = view;
  document.getElementById('cards').classList.toggle('hidden', view !== 'cards');
  document.getElementById('tableWrap').classList.toggle('hidden', view !== 'table');
  document.getElementById('cardBtn').classList.toggle('active', view === 'cards');
  document.getElementById('tableBtn').classList.toggle('active', view === 'table');
  render();
}

function resetFilters() {
  document.getElementById('search').value = '';
  document.getElementById('country-filter').value = '';
  document.getElementById('priority-filter').value = '';
  document.getElementById('status-filter').value = '';
  render();
}

document.getElementById('search').addEventListener('input', render);
document.getElementById('country-filter').addEventListener('change', render);
document.getElementById('priority-filter').addEventListener('change', render);
document.getElementById('status-filter').addEventListener('change', render);

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


def normalize_country(raw):
    """Many 'Country' CSV cells are actually 'Country — City, Region (Address)' strings
    copied from the markdown Quick Facts 'Country / HQ' field. Strip that down to just
    the country name for filtering/display; full detail stays on the profile page."""
    c = (raw or "").strip()
    c = re.split(r"\s+[—–-]\s+", c, maxsplit=1)[0]
    c = re.sub(r"\s*\(.*$", "", c).strip()
    return c


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


def truncate(text, max_len):
    text = (text or "").strip()
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "…"


def build_index(rows):
    orgs_js = []
    for row in rows:
        slug = row.get("GitHub slug", "").strip() or slugify_fallback(row.get("Organisation", ""))
        orgs_js.append({
            "name": row.get("Organisation", "").strip(),
            "slug": slug,
            "country": normalize_country(row.get("Country", "")),
            "categories": row.get("Tags", "").strip() or row.get("Categories", "").strip(),
            "priority": row.get("REUSE priority rating", "").strip(),
            "summary": truncate(row.get("Short summary", "") or row.get("Core model", ""), 220),
            "year": truncate(row.get("Year founded", ""), 60),
            "status": row.get("Status", "").strip(),
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
