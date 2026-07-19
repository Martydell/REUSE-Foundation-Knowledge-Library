
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
