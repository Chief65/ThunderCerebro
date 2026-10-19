(() => {
'use strict';

/* =====================================================================
   Noera · Central — explorador de archivos de la carpeta Noera
   Sin dependencias. Todo el contenido de usuario se inserta con
   textContent o pasa por esc() antes de usar innerHTML.
   ===================================================================== */

const $ = (s, r = document) => r.querySelector(s);
const TOKEN = $('meta[name=noera-token]').content;
const enc = encodeURIComponent;
const VERSION = 'v1.3.0';
function readExpanded() {
  try { const v = JSON.parse(localStorage.getItem('noera.exp') || '[]'); return new Set(Array.isArray(v) ? v.filter(p => typeof p === 'string') : []); }
  catch { return new Set(); }
}
const PALETTE = ['#337ea9', '#9065b0', '#d9730d', '#448361', '#cb912f', '#c14c8a'];

const S = {
  tree: [], allowed: [],
  meta: { taggedFolders: {} },
  expanded: readExpanded(),
  sel: null,            // {path, type}
  cur: null,            // archivo abierto {path,name,content,mtime,size,dirty}
  loadErr: null,
  mode: 'read',         // 'read' | 'edit'
  filter: '',
  focusPath: null,
  drag: null,
  firstLoad: true,
  saving: false,
  selectionSeq: 0,
  noeraFilesLoaded: false, noeraChangelogLoaded: false,
  noeraFilesError: '', noeraChangelogError: '',
  noeraTab: 'files',
  noeraFiles: [],
  noeraSelFile: 0,
  noeraChangelog: [],
};

/* ---------------- utilidades ---------------- */
function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? '' : v);
  }
  for (const c of kids.flat()) if (c != null) n.append(c);
  return n;
}
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
const SVG = {
  chev: '<svg class="chev" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  dir: '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4.5A1.5 1.5 0 0 1 3.5 3H7l1.5 2h5A1.5 1.5 0 0 1 15 6.5v6a1.5 1.5 0 0 1-1.5 1.5h-10A1.5 1.5 0 0 1 2 12.5z" fill="currentColor"/></svg>',
  file: '<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.5h5L13 5.5v9H4z M9 1.5v4h4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>',
};
function icon(name, cls) {
  const t = document.createElement('template');
  t.innerHTML = SVG[name];
  const n = t.content.firstElementChild;
  if (cls) n.classList.add(cls);
  return n;
}
const pl = (n, s, p) => n + ' ' + (n === 1 ? s : p);
const fmtSize = b => b < 1024 ? b + ' B' : b < 1048576 ? (b / 1024).toFixed(1) + ' KB' : (b / 1048576).toFixed(1) + ' MB';
function fmtDate(ticks) {
  try {
    const ms = Number((BigInt(ticks) - 621355046400000000n) / 10000n);
    return new Date(ms).toLocaleString('es', { dateStyle: 'medium', timeStyle: 'short' });
  } catch { return ''; }
}
const parentOf = p => p.split('/').slice(0, -1).join('/');
const baseOf = p => p.split('/').pop();
const join = (d, n) => d ? d + '/' + n : n;

function toast(msg, kind = 'info') {
  const t = el('div', { class: 'toast ' + kind, text: msg });
  $('#toasts').append(t);
  setTimeout(() => t.remove(), kind === 'error' ? 6500 : 3200);
}
async function api(method, url, o = {}) {
  const opts = { method, headers: { 'X-Noera-Token': TOKEN } };
  if (o.json !== undefined) { opts.body = JSON.stringify(o.json); opts.headers['Content-Type'] = 'application/json'; }
  else if (o.body !== undefined) { opts.body = o.body; opts.headers['Content-Type'] = o.type || 'application/octet-stream'; }
  let res;
  try { res = await fetch(url, opts); }
  catch { throw new Error('No hay conexión con el servidor de Noera. ¿Sigue abierta la ventana de PowerShell?'); }
  let data = null;
  try { data = await res.json(); } catch { /* sin cuerpo */ }
  if (!res.ok) { const e = new Error((data && data.error) || ('Error ' + res.status)); e.status = res.status; throw e; }
  return data;
}
const guard = fn => async (...a) => { try { return await fn(...a); } catch (e) { toast(e.message || 'Error inesperado', 'error'); } };

/* ---------------- árbol: datos ---------------- */
function findNode(path, nodes = S.tree) {
  for (const n of nodes) {
    if (n.path === path) return n;
    if (n.type === 'dir' && path.startsWith(n.path + '/')) { const r = findNode(path, n.children); if (r) return r; }
  }
  return null;
}
function countNode(n) {
  let files = 0, dirs = 0;
  const walk = list => { for (const c of list) { if (c.type === 'dir') { dirs++; walk(c.children); } else files++; } };
  if (n.type === 'dir') walk(n.children); else files = 1;
  return { files, dirs };
}
function colorOf(path) {
  const top = path.split('/')[0];
  const i = S.tree.findIndex(n => n.name === top);
  return PALETTE[(i < 0 ? 0 : i) % PALETTE.length];
}
function dirOptions() {
  const o = [{ path: '', label: 'Noera (raíz)' }];
  (function walk(nodes, l) { for (const n of nodes) if (n.type === 'dir') { o.push({ path: n.path, label: '\u2003'.repeat(l) + n.name }); walk(n.children, l + 1); } })(S.tree, 1);
  return o;
}
function saveExpanded() { try { localStorage.setItem('noera.exp', JSON.stringify([...S.expanded])); } catch { /* almacenamiento opcional */ } }
function expandAncestors(path) {
  const parts = path.split('/'); parts.pop();
  let acc = '';
  for (const p of parts) { acc = join(acc, p); S.expanded.add(acc); }
  saveExpanded();
}
function remapPath(oldP, newP) {
  const m = p => p === oldP ? newP : p.startsWith(oldP + '/') ? newP + p.slice(oldP.length) : p;
  S.expanded = new Set([...S.expanded].map(m)); saveExpanded();
  if (S.sel) S.sel.path = m(S.sel.path);
  if (S.cur) { S.cur.path = m(S.cur.path); S.cur.name = baseOf(S.cur.path); }
  if (S.focusPath) S.focusPath = m(S.focusPath);
}

async function loadTree() {
  const [d, m] = await Promise.all([
    api('GET', '/api/tree'),
    api('GET', '/api/folder/meta').catch(() => ({ taggedFolders: {} }))
  ]);
  S.tree = d.tree; S.allowed = d.allowedExt;
  S.meta = m || { taggedFolders: {} };
  if (S.firstLoad) {
    S.firstLoad = false;
    if (!S.expanded.size) for (const n of S.tree) if (n.type === 'dir') S.expanded.add(n.path);
  }
  if (S.sel && S.sel.type !== 'noera_code' && !findNode(S.sel.path)) {
    if (S.cur?.dirty) toast('El archivo abierto ya no aparece en disco; conserva o copia tus cambios.', 'error');
    else { ++S.selectionSeq; S.sel = null; S.cur = null; S.mode = 'read'; }
  }
  renderAll();
}

/* ---------------- render: árbol ---------------- */
function matchTree(nodes, f) {
  const out = [];
  for (const n of nodes) {
    const hit = n.name.toLowerCase().includes(f);
    if (n.type === 'dir') {
      if (hit) out.push(n);
      else { const kids = matchTree(n.children, f); if (kids.length) out.push({ ...n, children: kids }); }
    } else if (hit) out.push(n);
  }
  return out;
}
function buildLi(n, level) {
  const isDir = n.type === 'dir';
  const open = isDir && (!!S.filter || S.expanded.has(n.path));
  const selected = S.sel && S.sel.path === n.path;
  const isUpdate = isDir && !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[n.path] && S.meta.taggedFolders[n.path].update);
  const li = el('li', { role: 'treeitem', 'aria-level': level, 'aria-selected': selected ? 'true' : 'false', tabindex: '-1', 'data-path': n.path, 'data-type': n.type });
  if (isDir) li.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (level === 1) li.style.setProperty('--c', colorOf(n.path));
  const row = el('div', { class: 'row' + (selected ? ' sel' : ''), draggable: 'true' });
  row.style.setProperty('--lvl', level - 1);
  row.append(isDir ? icon('chev') : icon('chev', 'none'), icon(isDir ? 'dir' : 'file'), el('span', { class: 'label', text: n.name, title: n.name }));
  if (isUpdate) row.append(el('span', { class: 'badge update-tag', text: 'Update' }));
  if (!isDir) row.append(el('span', { class: 'tag', text: n.ext.slice(1) }));
  li.append(row);
  if (isDir && open) {
    const g = el('ul', { role: 'group' });
    if (!n.children.length) { const e = el('li', { role: 'none', class: 'empty', text: 'Carpeta vacía' }); e.style.setProperty('--lvl', level); g.append(e); }
    n.children.forEach(c => g.append(buildLi(c, level + 1)));
    li.append(g);
  }
  return li;
}
function renderTree() {
  const tree = $('#tree');
  const had = tree.contains(document.activeElement);
  const list = S.filter ? matchTree(S.tree, S.filter.toLowerCase()) : S.tree;
  tree.replaceChildren();
  if (!list.length) tree.append(el('li', { role: 'none', class: 'empty', text: S.filter ? 'Sin coincidencias.' : 'Noera está vacía.' }));
  list.forEach(n => tree.append(buildLi(n, 1)));
  const items = [...tree.querySelectorAll('li[role=treeitem]')];
  const target = items.find(i => i.dataset.path === S.focusPath) || items.find(i => i.dataset.path === (S.sel && S.sel.path)) || items[0];
  if (target) { target.tabIndex = 0; if (had) target.focus({ preventScroll: true }); }
}
function setRoving(li) {
  $('#tree').querySelectorAll('li[tabindex="0"]').forEach(x => x.tabIndex = -1);
  li.tabIndex = 0;
}

/* ---------------- render: barra superior / estado ---------------- */
function renderTopbar() {
  const c = $('#crumbs'), a = $('#actions');
  c.replaceChildren(); a.replaceChildren();
  const B = (txt, fn, cls = '') => el('button', { type: 'button', class: 'btn ' + cls, onclick: guard(fn) }, txt);

  if (S.sel && S.sel.type === 'noera_code') {
    c.append(
      el('button', { type: 'button', onclick: guard(() => select('')) }, 'Noera'),
      el('span', { class: 'sep', 'aria-hidden': 'true', text: '›' }),
      el('span', { class: 'cur', 'aria-current': 'page', text: 'Código de Noera' })
    );
    a.append(
      el('span', { class: 'badge update-tag', text: VERSION + ' Activo' }),
      B('🚀 Actualizar Noera con ZIP', () => openZipUpdateDialog('__noera__')),
      B('📦 Descargar ZIP del Código', downloadNoeraZip, 'primary')
    );
    return;
  }

  const segs = S.sel ? S.sel.path.split('/') : [];
  c.append(segs.length ? el('button', { type: 'button', onclick: guard(() => select('')) }, 'Noera') : el('span', { class: 'cur', text: 'Noera' }));
  segs.forEach((s, i) => {
    c.append(el('span', { class: 'sep', 'aria-hidden': 'true', text: '›' }));
    if (i === segs.length - 1) c.append(el('span', { class: 'cur', 'aria-current': 'page', text: s }));
    else { const p = segs.slice(0, i + 1).join('/'); c.append(el('button', { type: 'button', onclick: guard(() => select(p)) }, s)); }
  });
  if (!S.sel) {
    a.append(
      B('🚀 Actualizar Noera con ZIP', () => openZipUpdateDialog('__noera__')),
      B('Descargar ZIP', () => downloadZip(''))
    );
    return;
  }
  if (S.sel.type === 'file') {
    a.append(B('Descargar archivo', () => downloadFile(S.sel.path)));
    if (S.cur) {
      a.append(el('div', { class: 'seg', role: 'group', 'aria-label': 'Modo' },
        el('button', { type: 'button', 'aria-pressed': S.mode === 'read', onclick: () => setMode('read') }, 'Leer'),
        el('button', { type: 'button', 'aria-pressed': S.mode === 'edit', onclick: () => setMode('edit') }, 'Editar')));
      a.append(B('Copiar', copyContent));
      if (S.mode === 'edit') { const sv = B('Guardar', () => save(), 'primary'); sv.disabled = !S.cur.dirty || S.saving; sv.id = 'btn-save'; a.append(sv); }
    }
  } else {
    const isUpdate = !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[S.sel.path] && S.meta.taggedFolders[S.sel.path].update);
    a.append(
      B('Carpeta', () => createIn(S.sel.path, 'dir')),
      B('Archivo', () => createIn(S.sel.path, 'file')),
      B('Subir', () => openUpload([], S.sel.path)),
      B('Descargar ZIP', () => downloadZip(S.sel.path)),
      B(isUpdate ? '✓ Etiqueta: Update' : 'Etiqueta: Update', () => toggleUpdateTag(S.sel.path), isUpdate ? 'primary' : '')
    );
    if (isUpdate) {
      a.append(B('🚀 Actualizar ZIP', () => openZipUpdateDialog(S.sel.path), 'primary'));
    }
  }
  a.append(B('Renombrar', () => renameItem(S.sel.path)), B('Eliminar', () => deleteItem(S.sel.path), 'danger'));
}
function renderStatus() {
  const s = $('#status'); s.replaceChildren();
  const l = el('span'), r = el('span');
  if (S.sel && S.sel.type === 'noera_code') {
    l.textContent = 'Código de Noera';
    r.textContent = VERSION + ' · Núcleo del Software Noera';
    s.append(l, r);
    return;
  }
  if (S.cur && S.sel && S.sel.type === 'file') {
    const lines = S.cur.content ? S.cur.content.split('\n').length : 0;
    l.textContent = S.sel.path;
    r.append(`${lines} líneas · ${S.cur.content.length} caracteres · UTF-8 `);
    if (S.cur.dirty) r.append(el('span', { class: 'badge warn', text: 'Sin guardar' }));
  } else if (S.sel) {
    const n = findNode(S.sel.path);
    l.textContent = S.sel.path;
    if (n) { const c = countNode(n); r.textContent = `${pl(c.files, 'archivo', 'archivos')} · ${pl(c.dirs, 'carpeta', 'carpetas')}`; }
  } else l.textContent = 'Noera';
  s.append(l, r);
}
function renderStats() {
  const c = countNode({ type: 'dir', children: S.tree });
  $('#stats').textContent = `${pl(c.files, 'archivo', 'archivos')} · ${pl(c.dirs, 'carpeta', 'carpetas')}`;
}

function overview() {
  const w = el('div', { class: 'hero' },
    el('h2', { text: 'Central Noera' }),
    el('p', { text: 'Explora, lee, edita y reorganiza los archivos de la carpeta Noera.' }));
  w.append(el('div', { class: 'hero-actions' },
    el('button', { type: 'button', class: 'btn', onclick: guard(() => createIn('', 'dir')) }, 'Nueva carpeta'),
    el('button', { type: 'button', class: 'btn primary', onclick: () => openUpload([], '') }, 'Subir archivos'),
    el('button', { type: 'button', class: 'btn', onclick: () => downloadZip('') }, 'Descargar ZIP'),
    el('button', { type: 'button', class: 'btn', onclick: () => openZipUpdateDialog('__noera__') }, '🚀 Actualizar Noera con ZIP')));
  const cards = el('div', { class: 'cards' });
  for (const n of S.tree) {
    if (n.type !== 'dir') continue;
    const c = countNode(n);
    const isUpdate = !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[n.path] && S.meta.taggedFolders[n.path].update);
    const titleKids = [el('h3', { text: n.name })];
    if (isUpdate) titleKids.push(el('span', { class: 'badge update-tag', text: 'Update' }));
    const card = el('button', { type: 'button', class: 'card', 'data-item-path': n.path, onclick: guard(() => { S.expanded.add(n.path); saveExpanded(); return select(n.path); }) },
      icon('dir'), ...titleKids, el('p', { text: `${pl(c.files, 'archivo', 'archivos')} · ${pl(c.dirs, 'subcarpeta', 'subcarpetas')}` }));
    card.style.setProperty('--c', colorOf(n.path));
    cards.append(card);
  }
  w.append(cards);
  return w;
}

function folderView(n) {
  const c = countNode(n);
  const isUpdate = !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[n.path] && S.meta.taggedFolders[n.path].update);
  const tagData = (S.meta && S.meta.taggedFolders && S.meta.taggedFolders[n.path]) || {};
  const history = tagData.history || [];

  const titleRow = el('div', { style: 'display: flex; align-items: center; gap: 10px; margin-bottom: 4px;' },
    el('h2', { text: n.name, style: 'margin: 0;' })
  );
  if (isUpdate) {
    titleRow.append(el('span', { class: 'badge update-tag', text: 'Update' }));
  }

  const w = el('div', { class: 'hero' },
    titleRow,
    el('p', { text: `${pl(c.files, 'archivo', 'archivos')} · ${pl(c.dirs, 'subcarpeta', 'subcarpetas')} · arrastra archivos aquí para subirlos` }));

  const heroActions = el('div', { class: 'hero-actions' },
    el('button', { type: 'button', class: 'btn', onclick: guard(() => createIn(n.path, 'dir')) }, 'Nueva carpeta'),
    el('button', { type: 'button', class: 'btn', onclick: guard(() => createIn(n.path, 'file')) }, 'Nuevo archivo'),
    el('button', { type: 'button', class: 'btn primary', onclick: () => openUpload([], n.path) }, 'Subir archivos'),
    el('button', { type: 'button', class: 'btn', onclick: () => downloadZip(n.path) }, 'Descargar ZIP'),
    el('button', { type: 'button', class: 'btn ' + (isUpdate ? 'primary' : ''), onclick: guard(() => toggleUpdateTag(n.path)) }, isUpdate ? '✓ Etiqueta: Update' : 'Poner Etiqueta: Update')
  );
  if (isUpdate) {
    heroActions.append(el('button', { type: 'button', class: 'btn primary', onclick: () => openZipUpdateDialog(n.path) }, '🚀 Actualizar con ZIP'));
  }
  w.append(heroActions);

  if (isUpdate) {
    const uz = el('div', { class: 'update-zone-card' },
      el('div', { class: 'update-zone-head' },
        el('div', { class: 'update-zone-title' },
          icon('dir'),
          el('span', { text: `Proyecto Vinculado a Actualización por ZIP (${n.name}.zip)` })
        ),
        el('div', { class: 'update-zone-actions' },
          el('button', { type: 'button', class: 'btn sm', onclick: () => downloadZip(n.path) }, `📦 Descargar ${n.name}.zip Actual`),
          el('button', { type: 'button', class: 'btn sm primary', onclick: () => openZipUpdateDialog(n.path) }, '🚀 Subir Nuevo ZIP y Sustituir')
        )
      ),
      el('p', { class: 'dlg-msg', text: `Puedes editar el proyecto en programas externos. Al terminar, comprime todo en "${n.name}.zip" y súbelo aquí. Se guardará un backup automático del ZIP anterior y los archivos en funcionamiento se sustituirán al instante.` })
    );

    if (history.length) {
      const histBox = el('div', { class: 'history-wrap' },
        el('div', { class: 'history-head-title' },
          el('span', { text: `Historial de Versiones & Backups Guardados (${history.length})` })
        )
      );
      const histList = el('div', { class: 'gh-history-list' });
      for (const h of history) {
        histList.append(el('div', { class: 'gh-history-row' },
          el('div', { class: 'gh-history-info' },
            el('span', { class: 'gh-tag', text: h.zipName }),
            el('span', { class: 'gh-history-date', text: h.date }),
            el('span', { class: 'gh-commit-hash', text: `${fmtSize(h.newSize)} subidos · backup ${fmtSize(h.backupSize)}` })
          ),
          el('button', { type: 'button', class: 'btn sm', onclick: () => downloadBackupZip(h.backupRel, `${n.name}_backup_${h.id}.zip`) }, 'Descargar Backup')
        ));
      }
      histBox.append(histList);
      uz.append(histBox);
    }
    w.append(uz);
  }

  const list = el('div', { class: 'flist' });
  list.append(el('div', { class: 'frow fhead' }, el('span', { text: 'Nombre' }), el('span', { text: 'Tamaño' }), el('span', { text: 'Modificado' })));
  if (!n.children.length) list.append(el('div', { class: 'emptybox', text: 'Carpeta vacía. Usa "Subir" o "Archivo" para añadir contenido.' }));
  for (const ch of n.children) {
    const ic = icon(ch.type === 'dir' ? 'dir' : 'file');
    ic.style.setProperty('--c', colorOf(ch.path));
    const isChUpdate = ch.type === 'dir' && !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[ch.path] && S.meta.taggedFolders[ch.path].update);
    const row = el('button', { type: 'button', class: 'frow', 'data-item-path': ch.path, onclick: guard(() => { if (ch.type === 'dir') { S.expanded.add(ch.path); saveExpanded(); } return select(ch.path); }) },
      el('span', { class: 'name' }, ic, el('span', { text: ch.name, title: ch.name }), isChUpdate ? el('span', { class: 'badge update-tag', text: 'Update' }) : null),
      el('span', { class: 'm', text: ch.type === 'file' ? fmtSize(ch.size) : '—' }),
      el('span', { class: 'm', text: fmtDate(ch.mtime) }));
    list.append(row);
  }
  w.append(list);
  return w;
}

function renderNoeraCodeView() {
  const wrap = el('div', { class: 'noera-view-wrap' });

  const headBox = el('div', { class: 'noera-header-box' },
    el('div', null,
      el('h2', null,
        el('span', { text: 'Código del Software Noera' })
      ),
      el('p', { class: 'dlg-msg', text: 'Explorador en tiempo real de los componentes del software Noera, descarga del código y registro histórico de cambios estilo GitHub.' })
    ),
    el('div', { style: 'display: flex; gap: 8px; flex-shrink: 0;' },
      el('button', { type: 'button', class: 'btn', onclick: () => openZipUpdateDialog('__noera__') }, '🚀 Actualizar Noera con ZIP'),
      el('button', { type: 'button', class: 'btn primary', onclick: downloadNoeraZip }, '📦 Descargar ZIP del Código')
    )
  );
  wrap.append(headBox);

  const activeTab = S.noeraTab || 'files';
  const noeraHistory = (S.meta && S.meta.taggedFolders && S.meta.taggedFolders._noera && S.meta.taggedFolders._noera.history) || [];

  const tabs = el('div', { class: 'sub-tabs' },
    el('button', {
      type: 'button',
      class: 'sub-tab-btn ' + (activeTab === 'files' ? 'active' : ''),
      onclick: () => { S.noeraTab = 'files'; renderViewer(); }
    }, '💻 Archivos en Tiempo Real (' + (S.noeraFiles ? S.noeraFiles.length : '...') + ')'),
    el('button', {
      type: 'button',
      class: 'sub-tab-btn ' + (activeTab === 'changelog' ? 'active' : ''),
      onclick: () => { S.noeraTab = 'changelog'; renderViewer(); }
    }, '📋 Cambios Realizados (Estilo GitHub)'),
    el('button', {
      type: 'button',
      class: 'sub-tab-btn ' + (activeTab === 'history' ? 'active' : ''),
      onclick: () => { S.noeraTab = 'history'; renderViewer(); }
    }, '🛡️ Historial de Backups (' + noeraHistory.length + ')')
  );
  wrap.append(tabs);

  if (activeTab === 'files') {
    if (!S.noeraFilesLoaded) {
      wrap.append(el('div', { class: 'emptybox', text: 'Cargando archivos del software Noera…' }));
      loadNoeraFiles().then(() => { if (S.sel?.type === 'noera_code') renderViewer(); });
      return wrap;
    }
    if (S.noeraFilesError || !S.noeraFiles.length) {
      wrap.append(el('div', { class: 'emptybox', text: S.noeraFilesError || 'No hay archivos disponibles.' }, el('button', { class: 'btn', onclick: () => { S.noeraFilesLoaded = false; renderViewer(); } }, 'Reintentar')));
      return wrap;
    }
    const selIdx = Math.min(S.noeraSelFile || 0, S.noeraFiles.length - 1);
    const curFile = S.noeraFiles[selIdx];

    const layout = el('div', { class: 'live-code-layout' });
    const fileList = el('div', { class: 'live-file-list' });

    S.noeraFiles.forEach((f, idx) => {
      const btn = el('button', {
        type: 'button',
        class: 'live-file-item ' + (idx === selIdx ? 'active' : ''),
        onclick: () => { S.noeraSelFile = idx; renderViewer(); }
      },
        icon('file'),
        el('span', { text: f.name }),
        el('span', { class: 'tag', style: 'margin-left: auto;', text: fmtSize(f.size) })
      );
      fileList.append(btn);
    });
    layout.append(fileList);

    const contentBox = el('div', { class: 'live-file-content' });
    const metaBar = el('div', { class: 'live-file-meta' },
      el('span', { text: `${curFile.path} · ${curFile.content.split('\n').length} líneas · ${fmtSize(curFile.size)} · Modificado: ${fmtDate(curFile.mtime)}` }),
      el('button', {
        type: 'button',
        class: 'btn sm',
        onclick: async () => {
          try {
            await navigator.clipboard.writeText(curFile.content);
            toast('Código de ' + curFile.name + ' copiado al portapapeles', 'ok');
          } catch {
            toast('No se pudo acceder al portapapeles', 'error');
          }
        }
      }, 'Copiar Código')
    );
    const pre = el('pre', { class: 'live-code-pre' }, el('code', { text: curFile.content }));
    contentBox.append(metaBar, pre);
    layout.append(contentBox);

    wrap.append(layout);
  } else if (activeTab === 'history') {
    if (!noeraHistory.length) {
      wrap.append(el('div', { class: 'emptybox', text: 'No hay respaldos registrados todavía para el software Noera. Al realizar la primera actualización con ZIP, se guardará aquí el backup previo automáticamente.' }));
      return wrap;
    }

    const histBox = el('div', { class: 'history-wrap' },
      el('div', { class: 'history-head-title' },
        el('span', { text: `Respaldos y Versiones Previas de Noera (${noeraHistory.length})` })
      )
    );
    const histList = el('div', { class: 'gh-history-list' });
    for (const h of noeraHistory) {
      histList.append(el('div', { class: 'gh-history-row' },
        el('div', { class: 'gh-history-info' },
          el('span', { class: 'gh-tag', text: h.zipName }),
          el('span', { class: 'gh-history-date', text: h.date }),
          el('span', { class: 'gh-commit-hash', text: `${fmtSize(h.newSize)} subidos · backup ${fmtSize(h.backupSize)}` })
        ),
        el('button', { type: 'button', class: 'btn sm', onclick: () => downloadBackupZip(h.backupRel, `Noera_backup_${h.id}.zip`) }, 'Descargar Backup')
      ));
    }
    histBox.append(histList);
    wrap.append(histBox);
  } else {
    if (!S.noeraChangelogLoaded) {
      wrap.append(el('div', { class: 'emptybox', text: 'Cargando registro de cambios…' }));
      loadNoeraChangelog().then(() => { if (S.sel?.type === 'noera_code') renderViewer(); });
      return wrap;
    }

    if (S.noeraChangelogError || !S.noeraChangelog.length) {
      wrap.append(el('div', { class: 'emptybox', text: S.noeraChangelogError || 'Sin cambios registrados.' }, el('button', { class: 'btn', onclick: () => { S.noeraChangelogLoaded = false; renderViewer(); } }, 'Reintentar')));
      return wrap;
    }
    const timeline = el('div', { class: 'gh-timeline' });
    for (const rel of S.noeraChangelog) {
      const card = el('div', { class: 'gh-release-card' },
        el('div', { class: 'gh-dot' }),
        el('div', { class: 'gh-card-header' },
          el('div', { style: 'display: flex; align-items: center; gap: 8px;' },
            el('span', { class: 'gh-tag', text: rel.version }),
            el('span', { class: 'gh-commit-hash', text: '#' + rel.commit }),
            el('span', { style: 'font-size: 12px; color: var(--muted);', text: `por ${rel.author} el ${rel.date}` })
          ),
          el('span', { class: 'badge ' + (rel.tag === 'Release' ? 'update-tag' : 'warn'), text: rel.tag })
        ),
        el('h3', { class: 'gh-card-title', text: rel.title })
      );

      const list = el('ul', { class: 'gh-changes-list' });
      for (const ch of rel.changes) {
        list.append(el('li', { class: 'gh-change-item' },
          el('span', { class: 'gh-badge ' + ch.type, text: ch.type }),
          el('span', { text: ch.text })
        ));
      }
      card.append(list);
      timeline.append(card);
    }
    wrap.append(timeline);
  }

  return wrap;
}

function fileView() {
  if (S.loadErr) return el('div', { class: 'emptybox', text: S.loadErr },
    el('button', { class: 'btn', onclick: guard(() => downloadFile(S.sel.path)) }, 'Descargar archivo'));
  if (!S.cur) return el('div', { class: 'emptybox', text: 'Cargando archivo…' });
  const c = S.cur;
  if (S.mode === 'edit') {
    const ed = el('textarea', { id: 'editor', 'aria-label': 'Editar ' + c.name, spellcheck: 'false' });
    // Los textarea normalizan CRLF; conservamos la convención original al guardar.
    ed.value = c.content;
    ed.addEventListener('input', () => {
      c.content = ed.value.replace(/\n/g, c.eol || '\n');
      c.dirty = c.content !== c.savedContent;
      renderTopbar(); renderStatus();
    });
    return el('div', { class: 'editor-wrap' }, ed);
  }
  const wrap = el('article', { class: 'reader' });
  if (/\.md$/i.test(c.name)) {
    const md = el('div', { class: 'md' });
    md.innerHTML = mdToHtml(c.content); wrap.append(md);
  } else wrap.append(el('pre', { class: 'raw' }, el('code', { text: c.content })));
  return wrap;
}

function renderViewer() {
  const v = $('#viewer');
  v.replaceChildren();
  if (S.sel && S.sel.type === 'noera_code') v.append(renderNoeraCodeView());
  else if (!S.sel) v.append(overview());
  else if (S.sel.type === 'dir') { const n = findNode(S.sel.path); if (n) v.append(folderView(n)); }
  else v.append(fileView());
}
function renderAll() { renderTree(); renderTopbar(); renderViewer(); renderStatus(); renderStats(); }

/* ---------------- Markdown (seguro: escapa todo antes de generar HTML) ---------------- */
function inline(src) {
  const tokens = [];
  const token = html => { tokens.push(html); return '\u0000' + (tokens.length - 1) + '\u0000'; };
  let s = String(src).replace(/\u0000/g, '\ufffd');
  s = s.replace(/`([^`]+)`/g, (m, c) => token('<code>' + esc(c) + '</code>'));
  s = s.replace(/\[([^\]\u0000]+)\]\((https?:\/\/[^\s)\u0000]+)\)/g,
    (m, label, href) => token('<a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + '</a>'));
  s = esc(s).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(>])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>')
    .replace(/~~([^~]+)~~/g, '<del>$1</del>');
  return s.replace(/\u0000(\d+)\u0000/g, (m, i) => tokens[+i] || '');
}
const RE_LIST = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/;
const RE_HR = /^\s*([-*_])(\s*\1){2,}\s*$/;
const RE_FENCE = /^\s*(`{3,}|~{3,})(.*)$/;
const RE_TSEP = /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/;
function splitRow(l) {
  let t = l.trim();
  if (t.startsWith('|')) t = t.slice(1);
  if (t.endsWith('|') && !t.endsWith('\\|')) t = t.slice(0, -1);
  return t.split(/(?<!\\)\|/).map(x => x.trim().replace(/\\\|/g, '|'));
}
function isBlockStart(lines, i) {
  const l = lines[i];
  return /^#{1,6}\s/.test(l) || RE_FENCE.test(l) || RE_HR.test(l) || /^\s*>/.test(l) || RE_LIST.test(l) ||
    (l.includes('|') && i + 1 < lines.length && RE_TSEP.test(lines[i + 1]));
}
function parseList(lines, i) {
  const stack = []; let html = '';
  while (i < lines.length) {
    const l = lines[i];
    const m = l.match(RE_LIST);
    if (m) {
      const indent = m[1].replace(/\t/g, '    ').length;
      const tag = /\d/.test(m[2]) ? 'ol' : 'ul';
      while (stack.length && indent < stack[stack.length - 1].indent) html += '</li></' + stack.pop().tag + '>';
      if (!stack.length || indent > stack[stack.length - 1].indent) { stack.push({ indent, tag }); html += '<' + tag + '><li>'; }
      else html += '</li><li>';
      let txt = m[3];
      const task = txt.match(/^\[( |x|X)\]\s+(.*)$/);
      if (task) { html += '<input type="checkbox" disabled' + (task[1] !== ' ' ? ' checked' : '') + '> '; txt = task[2]; }
      html += inline(txt);
      i++;
    } else if (/^\s*$/.test(l)) {
      let j = i; while (j < lines.length && /^\s*$/.test(lines[j])) j++;
      if (j < lines.length && RE_LIST.test(lines[j])) i = j; else break;
    } else if (/^\s+\S/.test(l)) { html += ' ' + inline(l.trim()); i++; }
    else break;
  }
  while (stack.length) html += '</li></' + stack.pop().tag + '>';
  return { html, next: i };
}
function mdToHtml(src, depth = 0) {
  if (depth > 32) return '<pre>' + esc(src) + '</pre>';
  const lines = src.replace(/\r\n?/g, '\n').split('\n');
  const out = []; let i = 0;
  if (lines[0] === '---') {
    const end = lines.indexOf('---', 1);
    if (end > 0) { out.push('<pre class="fm"><code>' + esc(lines.slice(1, end).join('\n')) + '</code></pre>'); i = end + 1; }
  }
  while (i < lines.length) {
    const line = lines[i];
    if (/^\s*$/.test(line)) { i++; continue; }
    let m = line.match(RE_FENCE);
    if (m) {
      const mark = m[1];
      const buf = []; i++;
      while (i < lines.length) {
        const t = lines[i].trim();
        if (t.length >= mark.length && t[0] === mark[0] && t.split(t[0]).join('') === '') { i++; break; }
        buf.push(lines[i]); i++;
      }
      out.push('<pre><code>' + esc(buf.join('\n')) + '</code></pre>');
      continue;
    }
    if ((m = line.match(/^(#{1,6})\s+(.*?)\s*#*\s*$/))) { out.push(`<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`); i++; continue; }
    if (RE_HR.test(line)) { out.push('<hr>'); i++; continue; }
    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) { buf.push(lines[i].replace(/^\s*> ?/, '')); i++; }
      const cm = buf[0].match(/^\[!(\w+)\]\s*(.*)$/);
      if (cm) {
        const kind = cm[1].toLowerCase();
        const rest = [cm[2], ...buf.slice(1)].join('\n');
        out.push(`<blockquote class="callout ${esc(kind)}"><div class="callout-title">${esc(cm[1])}</div>${mdToHtml(rest, depth + 1)}</blockquote>`);
      } else out.push('<blockquote>' + mdToHtml(buf.join('\n'), depth + 1) + '</blockquote>');
      continue;
    }
    if (line.includes('|') && i + 1 < lines.length && RE_TSEP.test(lines[i + 1])) {
      const head = splitRow(line);
      const al = splitRow(lines[i + 1]).map(c => c.startsWith(':') && c.endsWith(':') ? 'center' : c.endsWith(':') ? 'right' : '');
      i += 2;
      let h = '<table><thead><tr>' + head.map((c, k) => `<th${al[k] ? ` class="al-${al[k]}"` : ''}>${inline(c)}</th>`).join('') + '</tr></thead><tbody>';
      while (i < lines.length && lines[i].includes('|') && !/^\s*$/.test(lines[i])) {
        h += '<tr>' + splitRow(lines[i]).map((c, k) => `<td${al[k] ? ` class="al-${al[k]}"` : ''}>${inline(c)}</td>`).join('') + '</tr>'; i++;
      }
      out.push(h + '</tbody></table>');
      continue;
    }
    if (RE_LIST.test(line)) { const r = parseList(lines, i); out.push(r.html); i = r.next; continue; }
    const buf = [line]; i++;
    while (i < lines.length && !/^\s*$/.test(lines[i]) && !isBlockStart(lines, i)) { buf.push(lines[i]); i++; }
    out.push('<p>' + buf.map((b, k) => inline(b.trim()) + (k < buf.length - 1 ? (/ {2,}$/.test(b) ? '<br>' : ' ') : '')).join('') + '</p>');
  }
  return out.join('\n');
}

/* ---------------- diálogo genérico ---------------- */
function ask({ title, message = '', label = null, value = '', okText = 'Aceptar', danger = false, validate = null, selectBase = false }) {
  return new Promise(resolve => {
    if ($('#dlg').open) { resolve(null); return; }
    const d = $('#dlg'), form = $('#dlg-form'), inp = $('#dlg-in'), err = $('#dlg-err'), ok = $('#dlg-ok'), cancel = $('#dlg-cancel');
    $('#dlg-title').textContent = title;
    $('#dlg-msg').textContent = message;
    $('#dlg-field').hidden = label === null;
    $('#dlg-lbl').textContent = label || '';
    inp.value = value; err.textContent = '';
    ok.textContent = okText;
    ok.classList.toggle('danger-solid', danger); ok.classList.toggle('primary', !danger);
    let done = false;
    const finish = v => {
      if (done) return; done = true;
      form.removeEventListener('submit', onSubmit); cancel.removeEventListener('click', onCancel); d.removeEventListener('cancel', onEsc);
      d.close(); resolve(v);
    };
    const onSubmit = e => {
      e.preventDefault();
      const v = label === null ? true : inp.value.trim();
      if (validate) { const m = validate(v); if (m) { err.textContent = m; inp.focus(); return; } }
      finish(v);
    };
    const onCancel = () => finish(null);
    const onEsc = e => { e.preventDefault(); finish(null); };
    form.addEventListener('submit', onSubmit); cancel.addEventListener('click', onCancel); d.addEventListener('cancel', onEsc);
    d.showModal();
    if (label !== null) { inp.focus(); if (selectBase) { const k = value.lastIndexOf('.'); inp.setSelectionRange(0, k > 0 ? k : value.length); } else inp.select(); }
    else (danger ? cancel : ok).focus();
  });
}
function validateName(v, isFile) {
  if (!v) return 'El nombre está vacío.';
  if (v.length > 120) return 'Nombre demasiado largo (máx. 120).';
  if (/[\\/:*?"<>|\u0000-\u001f]/.test(v)) return 'Caracteres no permitidos: \\ / : * ? " < > |';
  if (v.startsWith('.') || v.startsWith('_')) return 'No puede empezar con "." ni "_" (reservado).';
  if (v.endsWith('.') || v !== v.trim()) return 'No puede terminar en punto ni tener espacios en los extremos.';
  if (/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$/i.test(v)) return 'Nombre reservado de Windows.';
  if (isFile) { const m = v.match(/\.[^.]+$/); if (!m || !S.allowed.includes(m[0].toLowerCase())) return 'Extensión no permitida. Permitidas: ' + S.allowed.join(' '); }
  return null;
}

/* ---------------- selección y modos ---------------- */
function focusEditor() {
  const ed = $('#editor'); if (!ed) return;
  ed.focus({ preventScroll: true }); ed.setSelectionRange(0, 0); ed.scrollTop = 0;
}
async function confirmDiscard(nextPath) {
  if (S.saving) { toast('Espera a que termine el guardado.', 'info'); return false; }
  if (S.cur && S.cur.dirty && (!S.sel || S.sel.path !== nextPath)) {
    const ok = await ask({ title: 'Cambios sin guardar', message: `"${S.cur.name}" tiene cambios sin guardar. ¿Descartarlos?`, okText: 'Descartar', danger: true });
    return !!ok;
  }
  return true;
}
async function select(path, o = {}) {
  const seq = ++S.selectionSeq;
  if (!(await confirmDiscard(path)) || seq !== S.selectionSeq) return false;
  if (!path) { S.sel = null; S.cur = null; S.loadErr = null; S.mode = 'read'; renderAll(); return true; }
  const node = findNode(path);
  if (!node) { toast('El elemento ya no existe.', 'error'); await loadTree(); return false; }
  if (node.type === 'dir') { S.sel = { path, type: 'dir' }; S.cur = null; S.loadErr = null; S.mode = 'read'; }
  else if (S.cur && S.sel && S.sel.path === path) { if (o.edit) S.mode = 'edit'; }
  else {
    S.sel = { path, type: 'file' }; S.cur = null; S.loadErr = null; S.mode = 'read';
    try {
      const f = await api('GET', '/api/file?path=' + enc(path));
      if (seq !== S.selectionSeq) return false;
      S.cur = { savedContent: f.content, eol: f.content.includes('\r\n') ? '\r\n' : '\n', path: f.path, name: f.name, content: f.content, mtime: f.mtime, size: f.size, dirty: false };
      if (o.edit) S.mode = 'edit';
    } catch (e) { if (seq !== S.selectionSeq) return false; S.loadErr = e.message; }
  }
  S.focusPath = path; expandAncestors(path);
  renderAll();
  if (S.mode === 'edit') focusEditor();
  return true;
}
function setMode(m) {
  if (!S.cur || S.mode === m) return;
  S.mode = m; renderTopbar(); renderViewer(); renderStatus();
  if (m === 'edit') focusEditor();
}
async function save(force = false, c = S.cur) {
  if (!c || !c.dirty || S.saving) return;
  S.saving = true; renderTopbar();
  const content = c.content;
  let retry = false;
  try {
    const r = await api('PUT', '/api/file?path=' + enc(c.path) + (force ? '' : '&mtime=' + enc(c.mtime)), { body: content, type: 'text/plain; charset=utf-8' });
    c.mtime = r.mtime; c.size = r.size; c.savedContent = content; c.dirty = c.content !== content;
    const n = findNode(c.path); if (n) { n.mtime = r.mtime; n.size = r.size; }
    toast(c.dirty ? 'Versión guardada; quedan cambios nuevos sin guardar.' : 'Guardado', 'ok');
  } catch (e) {
    if (e.status === 409) {
      retry = !!(await ask({ title: 'El archivo cambió en disco', message: 'Otro programa modificó este archivo. ¿Sobrescribir con tu versión?', okText: 'Sobrescribir', danger: true }));
    } else toast(e.message, 'error');
  } finally { S.saving = false; renderTopbar(); renderStatus(); }
  if (retry && S.cur === c) return save(true, c);
}
async function copyContent() {
  if (!S.cur) return;
  try { await navigator.clipboard.writeText(S.cur.content); toast('Contenido copiado al portapapeles', 'ok'); }
  catch { toast('No se pudo acceder al portapapeles.', 'error'); }
}

/* ---------------- operaciones de archivos ---------------- */
async function createIn(dir, kind) {
  const isFile = kind === 'file';
  const name = await ask({
    title: isFile ? 'Nuevo archivo' : 'Nueva carpeta',
    message: dir ? 'En: ' + dir : 'En: Noera (raíz)',
    label: 'Nombre', value: isFile ? 'nuevo.md' : 'Nueva carpeta', okText: 'Crear', selectBase: isFile,
    validate: v => validateName(isFile && v && !/\.[^.]+$/.test(v) ? v + '.md' : v, isFile),
  });
  if (!name) return;
  const finalName = isFile && !/\.[^.]+$/.test(name) ? name + '.md' : name;
  const r = await api('POST', isFile ? '/api/newfile' : '/api/mkdir', { json: { path: join(dir, finalName) } });
  if (dir) { S.expanded.add(dir); saveExpanded(); }
  await loadTree();
  await select(r.path, { edit: isFile });
}
async function renameItem(path) {
  const n = findNode(path); if (!n) return;
  const isFile = n.type === 'file';
  const name = await ask({ title: 'Renombrar', message: path, label: 'Nuevo nombre', value: n.name, okText: 'Renombrar', selectBase: isFile, validate: v => validateName(v, isFile) });
  if (!name || name === n.name) return;
  if (S.cur && S.cur.dirty && (S.cur.path === path || S.cur.path.startsWith(path + '/'))) { toast('Guarda o descarta los cambios antes de renombrar.', 'error'); return; }
  const r = await api('POST', '/api/rename', { json: { path, newName: name } });
  remapPath(path, r.path);
  await loadTree();
  toast('Renombrado', 'ok');
}
async function deleteItem(path) {
  const n = findNode(path); if (!n) return;
  if (S.saving) { toast('Espera a que termine el guardado.', 'info'); return; }
  const c = countNode(n);
  const extra = n.type === 'dir' ? ` (${pl(c.files, 'archivo', 'archivos')}, ${pl(c.dirs, 'subcarpeta', 'subcarpetas')})` : '';
  const ok = await ask({ title: 'Eliminar', message: `"${n.name}"${extra} se moverá a la papelera de Noera (carpeta oculta .papelera). No se borra de forma definitiva.`, okText: 'Mover a la papelera', danger: true });
  if (!ok) return;
  if (S.cur && (S.cur.path === path || S.cur.path.startsWith(path + '/')) && !(await confirmDiscard(''))) return;
  await api('POST', '/api/delete', { json: { path } });
  if (S.sel && (S.sel.path === path || S.sel.path.startsWith(path + '/'))) { S.sel = null; S.cur = null; S.loadErr = null; S.mode = 'read'; }
  await loadTree();
  toast('Movido a la papelera', 'ok');
}
async function moveItem(from, toDir) {
  const n = findNode(from); if (!n) return;
  if (parentOf(from) === toDir) return;
  if (n.type === 'dir' && (toDir === from || toDir.startsWith(from + '/'))) { toast('No se puede mover una carpeta dentro de sí misma.', 'error'); return; }
  if (S.cur && S.cur.dirty && (S.cur.path === from || S.cur.path.startsWith(from + '/'))) { toast('Guarda o descarta los cambios antes de mover.', 'error'); return; }
  const r = await api('POST', '/api/move', { json: { from, toDir } });
  remapPath(from, r.path);
  if (toDir) { S.expanded.add(toDir); saveExpanded(); }
  await loadTree();
  toast(`Movido a ${toDir || 'Noera (raíz)'}`, 'ok');
}
async function download(url, filename) {
  const res = await fetch(url, { headers: { 'X-Noera-Token': TOKEN } });
  if (!res.ok) {
    let msg = 'Error ' + res.status;
    try { msg = (await res.json()).error || msg; } catch { /* respuesta sin JSON */ }
    throw new Error(msg);
  }
  const objectUrl = URL.createObjectURL(await res.blob());
  const a = el('a', { href: objectUrl, download: filename });
  document.body.append(a); a.click();
  setTimeout(() => { a.remove(); URL.revokeObjectURL(objectUrl); }, 60000);
  toast('Descarga preparada: ' + filename, 'ok');
}
const downloadZip = guard(dir => download('/api/zip?path=' + enc(dir), (dir ? baseOf(dir) : 'Noera') + '.zip'));
const downloadFile = guard(path => download('/api/download?path=' + enc(path), baseOf(path)));
const downloadNoeraZip = guard(() => download('/api/noera/zip', 'Noera-Software-Source.zip'));

async function loadNoeraFiles() {
  S.noeraFilesLoaded = true; S.noeraFilesError = '';
  try {
    const res = await api('GET', '/api/noera/files');
    S.noeraFiles = res.files || [];
    return S.noeraFiles;
  } catch (e) {
    S.noeraFilesError = 'Error cargando archivos de Noera: ' + e.message; toast(S.noeraFilesError, 'error');
    return [];
  }
}

async function loadNoeraChangelog() {
  S.noeraChangelogLoaded = true; S.noeraChangelogError = '';
  try {
    const res = await api('GET', '/api/noera/changelog');
    S.noeraChangelog = Array.isArray(res) ? res : (res && res.changelog ? res.changelog : []);
    return S.noeraChangelog;
  } catch (e) {
    S.noeraChangelogError = 'Error cargando historial de cambios: ' + e.message; toast(S.noeraChangelogError, 'error');
    return [];
  }
}

const downloadBackupZip = guard((path, filename) => download('/api/folder/history/download?file=' + enc(path), filename || 'backup.zip'));

async function toggleUpdateTag(folderPath) {
  try {
    const isUpdate = !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[folderPath] && S.meta.taggedFolders[folderPath].update);
    const res = await api('POST', '/api/folder/tag', {
      json: { path: folderPath, enabled: !isUpdate }
    });
    if (res && res.meta) S.meta = res.meta;
    await loadTree();
    renderAll();
    toast(!isUpdate ? `Etiqueta "Update" activada para "${baseOf(folderPath)}"` : `Etiqueta "Update" desactivada`, 'ok');
  } catch (e) {
    toast(e.message || 'Error al cambiar etiqueta.', 'error');
  }
}

let zipUpBusy = false;
let zipUpTarget = '';
let zipUpSelectedFile = null;

function openZipUpdateDialog(folderPath) {
  if (zipUpBusy) return;
  zipUpTarget = folderPath;
  zipUpSelectedFile = null;
  const isNoera = folderPath === '__noera__';
  const folderName = isNoera ? 'Noera Software' : baseOf(folderPath);
  const expectedZip = isNoera ? 'Noera-Software-Source.zip' : (folderName + '.zip');

  $('#zip-up-title').textContent = isNoera ? 'Actualizar Noera Software con ZIP' : `Actualizar "${folderName}" con ZIP`;
  $('#zip-up-desc').textContent = isNoera
    ? 'El archivo ZIP sustituirá los componentes operativos del software Noera (_app/ y launcher). Antes de sobrescribir, se guardará un respaldo automático del software actual en el historial de versiones.'
    : `El archivo ZIP sustituirá todos los archivos en funcionamiento de "${folderPath}". Antes de sobrescribir, se guardará un respaldo automático del ZIP actual en el historial de versiones.`;
  $('#zip-up-req').textContent = isNoera
    ? `Requisito estricto: El archivo debe llamarse exactamente "${expectedZip}" (o "Noera.zip").`
    : `Requisito estricto: El archivo debe llamarse exactamente "${expectedZip}".`;
  $('#zip-up-prompt').textContent = `Arrastra "${expectedZip}" aquí o`;
  $('#zip-up-input').value = '';
  $('#zip-up-file-info').hidden = true;
  $('#zip-up-err').textContent = '';
  $('#zip-up-ok').disabled = true;
  $('#zip-up-ok').textContent = 'Sustituir y Actualizar Ahora';
  const dlg = $('#zip-up-dlg');
  if (!dlg.open) dlg.showModal();
}

function handleZipSelected(file) {
  if (zipUpBusy || !file) return;
  zipUpSelectedFile = null;
  const isNoera = zipUpTarget === '__noera__';
  const folderName = isNoera ? 'Noera Software' : baseOf(zipUpTarget);
  const fileInfo = $('#zip-up-file-info');
  const errBox = $('#zip-up-err');
  const btnOk = $('#zip-up-ok');

  fileInfo.hidden = true;
  errBox.textContent = '';
  btnOk.disabled = true;

  if (!file.name.toLowerCase().endsWith('.zip')) {
    errBox.textContent = `Error: El archivo debe ser de formato .ZIP. Recibido: "${file.name}".`;
    return;
  }

  if (isNoera) {
    const validNames = ['noera-software-source.zip', 'noera.zip'];
    if (!validNames.includes(file.name.toLowerCase())) {
      errBox.textContent = `Error: El archivo debe llamarse exactamente "Noera-Software-Source.zip" (o "Noera.zip"). Recibido: "${file.name}".`;
      return;
    }
  } else {
    const expectedZip = (folderName + '.zip').toLowerCase();
    if (file.name.toLowerCase() !== expectedZip) {
      errBox.textContent = `Error: El nombre del archivo debe ser exactamente "${folderName}.zip". El archivo seleccionado se llama "${file.name}".`;
      return;
    }
  }

  if (file.size > 150 * 1048576 || file.size < 22) { errBox.textContent = 'El ZIP debe tener entre 22 bytes y 150 MB.'; return; }
  zipUpSelectedFile = file;
  fileInfo.hidden = false;
  fileInfo.replaceChildren(
    el('div', { style: 'display: flex; align-items: center; justify-content: space-between; padding: 4px 0;' },
      el('span', { style: 'font-weight: 600; color: var(--accent);', text: '✓ Archivo válido: ' + file.name }),
      el('span', { class: 'tag', text: fmtSize(file.size) })
    )
  );
  btnOk.disabled = false;
}

async function executeZipUpdate() {
  if (zipUpBusy || !zipUpSelectedFile || !zipUpTarget || S.saving) return;
  const isNoera = zipUpTarget === '__noera__';
  const folderName = isNoera ? 'Noera Software' : baseOf(zipUpTarget);
  if (!isNoera && S.cur && S.cur.path.startsWith(zipUpTarget + '/') && !(await confirmDiscard(''))) return;
  if (zipUpBusy) return;
  zipUpBusy = true;
  $('#zip-up-cancel').disabled = true; $('#zip-up-pick').disabled = true;
  const btnOk = $('#zip-up-ok');
  const errBox = $('#zip-up-err');
  btnOk.disabled = true;
  btnOk.textContent = 'Actualizando y sustituyendo…';
  toast(`Subiendo "${zipUpSelectedFile.name}" y actualizando…`, 'info');

  try {
    const endpoint = isNoera
      ? `/api/noera/update-zip?name=${enc(zipUpSelectedFile.name)}`
      : `/api/folder/update-zip?path=${enc(zipUpTarget)}&name=${enc(zipUpSelectedFile.name)}`;

    const res = await api('POST', endpoint, {
      body: zipUpSelectedFile,
      type: 'application/zip'
    });
    if (res && res.meta) S.meta = res.meta;

    if (isNoera) {
      $('#zip-up-dlg').close();
      toast('Software Noera actualizado con éxito. Respaldo guardado. Reiniciando vista…', 'ok');
      await loadNoeraFiles();
      await loadNoeraChangelog();
      setTimeout(() => location.reload(), 1200);
      return;
    }

    if (S.cur && (S.cur.path === zipUpTarget || S.cur.path.startsWith(zipUpTarget + '/'))) { S.cur = null; S.sel = { path: zipUpTarget, type: 'dir' }; S.mode = 'read'; }
    $('#zip-up-dlg').close();
    toast(`Proyecto "${folderName}" actualizado con éxito. Respaldo creado en historial.`, 'ok');
    await loadTree();
    renderAll();
  } catch (e) {
    errBox.textContent = e.message || 'Error al actualizar con ZIP.';
    btnOk.disabled = false;
    btnOk.textContent = 'Sustituir y Actualizar Ahora';
    toast(e.message || 'Error al actualizar.', 'error');
  } finally { zipUpBusy = false; $('#zip-up-cancel').disabled = false; $('#zip-up-pick').disabled = false; }
}

/* ---------------- subida de archivos ---------------- */
const U = { items: [], busy: false, seq: 0 };
const MAX_UP = 25 * 1048576;
function fillDestSelect(sel, value) {
  sel.replaceChildren();
  for (const o of dirOptions()) sel.append(el('option', { value: o.path, text: o.label }));
  sel.value = value;
}
function addFiles(files, dest) {
  if (U.busy) return;
  for (const f of files) {
    const it = { id: ++U.seq, file: f, name: f.name, dest, status: 'pending', msg: '' };
    const ext = (f.name.match(/\.[^.]+$/) || [''])[0].toLowerCase();
    if (!S.allowed.includes(ext)) { it.status = 'error'; it.msg = `Extensión no permitida (${ext || 'sin extensión'}).`; }
    else if (f.size > MAX_UP) { it.status = 'error'; it.msg = 'Supera el máximo de 25 MB.'; }
    U.items.push(it);
  }
  renderUpload();
}
function renderUpload() {
  const ul = $('#up-list'); ul.replaceChildren();
  if (!U.items.length) ul.append(el('li', { class: 'emptybox', text: 'No hay archivos en la cola.' }));
  for (const it of U.items) {
    const locked = U.busy || it.status === 'ok';
    const name = el('input', { value: it.name, 'aria-label': 'Nombre de ' + it.file.name, disabled: locked, spellcheck: 'false' });
    name.addEventListener('input', () => { it.name = name.value; if (it.status === 'error') { it.status = 'pending'; it.msg = ''; st.textContent = stText(it); li.className = 'up-item ' + it.status; } });
    const sel = el('select', { 'aria-label': 'Destino de ' + it.file.name, disabled: locked });
    fillDestSelect(sel, it.dest);
    sel.addEventListener('change', () => { it.dest = sel.value; });
    const rm = el('button', { type: 'button', class: 'btn sm', disabled: U.busy, onclick: () => { U.items = U.items.filter(x => x !== it); renderUpload(); } }, 'Quitar');
    const st = el('div', { class: 'st', text: stText(it) });
    const li = el('li', { class: 'up-item ' + it.status }, name, sel, rm, st);
    ul.append(li);
  }
  $('#up-go').disabled = U.busy || !U.items.some(i => i.status === 'pending');
  $('#up-pick').disabled = U.busy; $('#up-close').disabled = U.busy; $('#up-dest-all').disabled = U.busy;
}
function stText(it) {
  return it.status === 'pending' ? `Listo para subir · ${fmtSize(it.file.size)}` : it.status === 'uploading' ? 'Subiendo…' : it.msg;
}
function openUpload(files, dest) {
  if (!U.busy) U.items = U.items.filter(i => i.status !== 'ok');
  $('#up-hint').textContent = 'Permitidos: ' + S.allowed.join(' ') + ' · máx. 25 MB por archivo';
  fillDestSelect($('#up-dest-all'), dest);
  addFiles([...files], dest);
  renderUpload();
  const d = $('#up-dlg'); if (!d.open) d.showModal();
}
async function uploadAll() {
  if (U.busy) return;
  U.busy = true; renderUpload();
  let ok = 0, bad = 0;
  for (const it of U.items) {
    if (it.status !== 'pending') continue;
    const v = validateName(it.name.trim(), true);
    if (v || it.file.size > MAX_UP) { it.status = 'error'; it.msg = v || 'Supera el máximo de 25 MB.'; bad++; continue; }
    it.status = 'uploading'; renderUpload();
    try {
      const r = await api('POST', `/api/upload?dir=${enc(it.dest)}&name=${enc(it.name.trim())}`, { body: it.file });
      it.status = 'ok'; it.msg = 'Subido como ' + r.path; ok++;
      if (it.dest) S.expanded.add(it.dest);
    } catch (e) { it.status = 'error'; it.msg = e.message; bad++; }
  }
  U.busy = false; saveExpanded(); renderUpload();
  try { await loadTree(); } catch (e) { toast(e.message, 'error'); }
  toast(`${ok} subido(s)` + (bad ? `, ${bad} con error` : ''), bad ? 'error' : 'ok');
}

/* ---------------- menú contextual ---------------- */
function closeCtx() { const m = $('#ctx'); if (!m.hidden) { m.hidden = true; m.replaceChildren(); } }
function openCtx(x, y, path) {
  const n = findNode(path); if (!n) return;
  const m = $('#ctx'); m.replaceChildren();
  const B = (t, fn, cls = '') => el('button', { type: 'button', role: 'menuitem', class: cls, onclick: () => { closeCtx(); guard(fn)(); } }, t);
  m.append(B('Abrir', () => { if (n.type === 'dir') { S.expanded.add(path); saveExpanded(); } return select(path); }));
  if (n.type === 'dir') {
    const isUpdate = !!(S.meta && S.meta.taggedFolders && S.meta.taggedFolders[path] && S.meta.taggedFolders[path].update);
    m.append(
      B('Nueva carpeta aquí', () => createIn(path, 'dir')),
      B('Nuevo archivo aquí', () => createIn(path, 'file')),
      B('Subir archivos aquí…', () => openUpload([], path)),
      B('Descargar como ZIP', () => downloadZip(path)),
      B(isUpdate ? 'Desactivar etiqueta Update' : 'Activar etiqueta Update', () => toggleUpdateTag(path))
    );
    if (isUpdate) {
      m.append(B('🚀 Actualizar con ZIP', () => openZipUpdateDialog(path)));
    }
  } else {
    m.append(B('Descargar archivo', () => downloadFile(path)), B('Editar', () => select(path, { edit: true })), B('Copiar contenido', async () => { if (await select(path)) await copyContent(); }));
  }
  m.append(el('hr'), B('Renombrar (F2)', () => renameItem(path)), B('Eliminar (Supr)', () => deleteItem(path), 'danger'));
  m.hidden = false;
  const r = m.getBoundingClientRect();
  m.style.left = Math.max(4, Math.min(x, innerWidth - r.width - 8)) + 'px';
  m.style.top = Math.max(4, Math.min(y, innerHeight - r.height - 8)) + 'px';
  m.querySelector('button').focus();
}

/* ---------------- eventos ---------------- */
function wire() {
  const tree = $('#tree');

  tree.addEventListener('click', guard(async e => {
    const li = e.target.closest('li[role=treeitem]'); if (!li) return;
    const path = li.dataset.path, isDir = li.dataset.type === 'dir';
    if (isDir && e.target.closest('.chev')) { toggle(path); return; }
    if (isDir && !S.filter) { if (S.expanded.has(path)) S.expanded.delete(path); else S.expanded.add(path); saveExpanded(); }
    await select(path);
  }));
  tree.addEventListener('focusin', e => { const li = e.target.closest('li[role=treeitem]'); if (li) { S.focusPath = li.dataset.path; setRoving(li); } });
  tree.addEventListener('contextmenu', e => {
    const li = e.target.closest('li[role=treeitem]'); if (!li) return;
    e.preventDefault(); S.focusPath = li.dataset.path;
    openCtx(e.clientX, e.clientY, li.dataset.path);
  });
  tree.addEventListener('keydown', guard(async e => {
    const li = e.target.closest('li[role=treeitem]'); if (!li || e.target !== li) return;
    const items = [...tree.querySelectorAll('li[role=treeitem]')];
    const idx = items.indexOf(li), path = li.dataset.path, isDir = li.dataset.type === 'dir';
    const focus = i => { const t = items[Math.max(0, Math.min(items.length - 1, i))]; if (t) t.focus(); };
    if (e.shiftKey && e.key === 'F10') { e.preventDefault(); const r = li.getBoundingClientRect(); openCtx(r.left, r.bottom, path); return; }
    switch (e.key) {
      case 'ArrowDown': e.preventDefault(); focus(idx + 1); break;
      case 'ArrowUp': e.preventDefault(); focus(idx - 1); break;
      case 'Home': e.preventDefault(); focus(0); break;
      case 'End': e.preventDefault(); focus(items.length - 1); break;
      case 'ArrowRight':
        e.preventDefault();
        if (isDir && !S.expanded.has(path) && !S.filter) toggle(path); else if (isDir) focus(idx + 1);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        if (isDir && S.expanded.has(path) && !S.filter) toggle(path);
        else { const p = items.findIndex(x => x.dataset.path === parentOf(path)); if (p >= 0) focus(p); }
        break;
      case 'Enter': case ' ': e.preventDefault(); await select(path); break;
      case 'ContextMenu':
        e.preventDefault(); { const r = li.getBoundingClientRect(); openCtx(r.left, r.bottom, path); } break;
      case 'F2': e.preventDefault(); await renameItem(path); break;
      case 'Delete': e.preventDefault(); await deleteItem(path); break;
      default: break;
    }
  }));

  /* arrastrar y soltar: mover (interno) o subir (archivos del sistema) */
  const dropTarget = e => {
    const li = e.target.closest('li[role=treeitem]');
    if (!li) return { dir: '', row: null };
    const isDir = li.dataset.type === 'dir';
    return { dir: isDir ? li.dataset.path : parentOf(li.dataset.path), row: isDir ? li.querySelector(':scope > .row') : null };
  };
  const clearDrop = () => { tree.classList.remove('drop-root'); tree.querySelectorAll('.row.drop').forEach(r => r.classList.remove('drop')); };
  tree.addEventListener('dragstart', e => {
    const li = e.target.closest('li[role=treeitem]'); if (!li) return;
    S.drag = li.dataset.path; e.dataTransfer.setData('application/x-noera', S.drag); e.dataTransfer.effectAllowed = 'move';
  });
  tree.addEventListener('dragend', () => { S.drag = null; clearDrop(); });
  tree.addEventListener('dragover', e => {
    const hasFiles = [...(e.dataTransfer.types || [])].includes('Files');
    if (!S.drag && !hasFiles) return;
    e.preventDefault(); e.dataTransfer.dropEffect = S.drag ? 'move' : 'copy';
    clearDrop();
    const t = dropTarget(e);
    if (t.row) t.row.classList.add('drop'); else tree.classList.add('drop-root');
  });
  tree.addEventListener('dragleave', e => { if (!tree.contains(e.relatedTarget)) clearDrop(); });
  tree.addEventListener('drop', guard(async e => {
    e.preventDefault(); clearDrop();
    const t = dropTarget(e);
    if (S.drag) { const from = S.drag; S.drag = null; await moveItem(from, t.dir); }
    else if (e.dataTransfer.files && e.dataTransfer.files.length) openUpload(e.dataTransfer.files, t.dir);
  }));

  /* subir archivos soltándolos sobre una carpeta abierta en el visor */
  const viewer = $('#viewer');
  viewer.addEventListener('contextmenu', e => {
    const item = e.target.closest('[data-item-path]');
    if (!item) return;
    e.preventDefault(); openCtx(e.clientX, e.clientY, item.dataset.itemPath);
  });
  viewer.addEventListener('keydown', e => {
    if (e.key !== 'ContextMenu' && !(e.shiftKey && e.key === 'F10')) return;
    const item = e.target.closest('[data-item-path]');
    if (!item) return;
    e.preventDefault(); const r = item.getBoundingClientRect(); openCtx(r.left, r.bottom, item.dataset.itemPath);
  });
  viewer.addEventListener('dragover', e => {
    if (!(S.sel && S.sel.type === 'dir') && S.sel) return;
    if (![...(e.dataTransfer.types || [])].includes('Files')) return;
    e.preventDefault(); viewer.classList.add('drop');
  });
  viewer.addEventListener('dragleave', e => { if (!viewer.contains(e.relatedTarget)) viewer.classList.remove('drop'); });
  viewer.addEventListener('drop', e => {
    viewer.classList.remove('drop');
    if (!e.dataTransfer.files || !e.dataTransfer.files.length) return;
    if (S.sel && S.sel.type !== 'dir') return;
    e.preventDefault(); openUpload(e.dataTransfer.files, S.sel ? S.sel.path : '');
  });

  $('#filter').addEventListener('input', e => { S.filter = e.target.value.trim(); renderTree(); });
  $('#btn-newdir').addEventListener('click', guard(() => createIn(selDir(), 'dir')));
  $('#btn-newfile').addEventListener('click', guard(() => createIn(selDir(), 'file')));
  $('#btn-upload').addEventListener('click', () => openUpload([], selDir()));

  /* código de noera */
  const btnNoera = $('#btn-noera-code');
  if (btnNoera) {
    btnNoera.addEventListener('click', guard(async () => {
      if (!(await confirmDiscard(''))) return;
      ++S.selectionSeq;
      S.sel = { path: '', type: 'noera_code' };
      S.cur = null;
      S.loadErr = null;
      S.mode = 'read';
      renderAll();
    }));
  }

  /* diálogo de subida */
  const drop = $('#up-drop'), input = $('#up-input');
  $('#up-pick').addEventListener('click', () => input.click());
  input.addEventListener('change', () => { addFiles([...input.files], $('#up-dest-all').value); input.value = ''; });
  drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('over'); });
  drop.addEventListener('dragleave', () => drop.classList.remove('over'));
  drop.addEventListener('drop', e => { e.preventDefault(); drop.classList.remove('over'); addFiles([...e.dataTransfer.files], $('#up-dest-all').value); });
  $('#up-dest-all').addEventListener('change', e => { if (U.busy) return; U.items.forEach(i => { if (i.status !== 'ok') i.dest = e.target.value; }); renderUpload(); });
  $('#up-go').addEventListener('click', guard(uploadAll));
  $('#up-close').addEventListener('click', () => { if (!U.busy) $('#up-dlg').close(); });
  $('#up-dlg').addEventListener('cancel', e => { if (U.busy) e.preventDefault(); });

  /* diálogo de actualización rápida con ZIP */
  const zipDrop = $('#zip-up-drop'), zipInput = $('#zip-up-input');
  $('#zip-up-pick').addEventListener('click', () => zipInput.click());
  zipInput.addEventListener('change', () => {
    if (zipInput.files && zipInput.files.length) handleZipSelected(zipInput.files[0]);
  });
  zipDrop.addEventListener('dragover', e => { e.preventDefault(); zipDrop.classList.add('over'); });
  zipDrop.addEventListener('dragleave', () => zipDrop.classList.remove('over'));
  zipDrop.addEventListener('drop', e => {
    e.preventDefault();
    zipDrop.classList.remove('over');
    if (e.dataTransfer.files && e.dataTransfer.files.length) handleZipSelected(e.dataTransfer.files[0]);
  });
  $('#zip-up-ok').addEventListener('click', guard(executeZipUpdate));
  $('#zip-up-cancel').addEventListener('click', () => { if (!zipUpBusy) $('#zip-up-dlg').close(); });
  $('#zip-up-dlg').addEventListener('cancel', e => { if (zipUpBusy) e.preventDefault(); });

  document.addEventListener('pointerdown', e => { if (!e.target.closest('#ctx')) closeCtx(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' || e.key === 'Tab') { const m = $('#ctx'); if (!m.hidden) { closeCtx(); const t = $('#tree li[tabindex="0"]'); if (t) t.focus(); } }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's' && S.cur && S.mode === 'edit') { e.preventDefault(); guard(() => save())(); }
  });
  $('#ctx').addEventListener('keydown', e => {
    const btns = [...$('#ctx').querySelectorAll('button')]; const i = btns.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); btns[(i + 1) % btns.length].focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); btns[(i - 1 + btns.length) % btns.length].focus(); }
  });
  window.addEventListener('beforeunload', e => { if ((S.cur && S.cur.dirty) || S.saving || zipUpBusy || U.busy) { e.preventDefault(); e.returnValue = ''; } });
  window.addEventListener('scroll', e => { if (!$('#ctx').contains(e.target)) closeCtx(); }, true);
}
function selDir() {
  if (!S.sel) return '';
  return S.sel.type === 'dir' ? S.sel.path : parentOf(S.sel.path);
}
function toggle(path) {
  if (S.expanded.has(path)) S.expanded.delete(path); else S.expanded.add(path);
  saveExpanded(); S.focusPath = path; renderTree();
}

/* ---------------- arranque ---------------- */
async function openFromHash() {
  let h; try { h = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  if (!h) return;
  const [p, m] = h.split('|');
  if (findNode(p)) await select(p, { edit: m === 'edit' });
}
wire();
loadTree().then(openFromHash).catch(e => {
  $('#viewer').replaceChildren(el('div', { class: 'emptybox', text: e.message }));
  toast(e.message, 'error');
});
})();
