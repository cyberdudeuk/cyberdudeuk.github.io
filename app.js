/* Launchpad: search, filters by area, level and live site, sorting, view and menu switches, the theme switch and motion.
   Everything is readable without this script. Nothing is stored except a theme you choose with the switch. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
  var $ = function (q) { return document.querySelector(q); };
  var $$ = function (q) { return Array.prototype.slice.call(document.querySelectorAll(q)); };
  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* Filtering */
  var cards = $$('.card'), blocks = $$('.cat-block'), cchips = $$('.cchip'), lchips = $$('.lchip');
  var shown = $('#shown'), empty = $('#empty'), q = $('#q'), live = $('#liveToggle'), projects = $('#projects');
  var state = { cat: 'all', level: 'all', q: '', live: false };
  function text(k) { return (k.textContent || '').toLowerCase(); }
  function apply() {
    cchips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-cat') === state.cat)); });
    lchips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-level') === state.level)); });
    if (live) live.setAttribute('aria-checked', String(state.live));
    var words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    var n = 0;
    blocks.forEach(function (b) {
      var any = false;
      b.querySelectorAll('.card').forEach(function (k) {
        var t = text(k);
        var on = (state.cat === 'all' || k.dataset.category === state.cat) &&
                 (state.level === 'all' || (' ' + k.dataset.levels + ' ').indexOf(' ' + state.level + ' ') > -1) &&
                 (!state.live || k.dataset.site === 'yes') &&
                 words.every(function (w) { return t.indexOf(w) > -1; });
        k.hidden = !on;
        if (on) { any = true; n += 1; }
      });
      b.hidden = !any;
    });
    if (shown) shown.textContent = n === cards.length ? 'Showing all ' + n + ' projects' : 'Showing ' + n + ' of ' + cards.length + ' projects';
    if (empty) empty.hidden = n !== 0;
  }
  function reset() { state = { cat: 'all', level: 'all', q: '', live: false }; if (q) q.value = ''; apply(); }
  function toProjects() { if (projects) projects.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }); }
  cchips.forEach(function (c) { c.addEventListener('click', function () { state.cat = c.getAttribute('data-cat'); apply(); }); });
  lchips.forEach(function (c) { c.addEventListener('click', function () { state.level = c.getAttribute('data-level'); apply(); }); });
  if (live) live.addEventListener('click', function () { state.live = !state.live; apply(); });
  if (q) {
    q.addEventListener('input', function () { state.q = q.value; apply(); });
    q.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') { q.value = ''; state.q = ''; apply(); } });
  }
  document.addEventListener('keydown', function (ev) {
    var tag = (ev.target && ev.target.tagName) || '';
    if (ev.key === '/' && q && !/INPUT|TEXTAREA|SELECT/.test(tag) && !ev.ctrlKey && !ev.metaKey && !ev.altKey) { ev.preventDefault(); q.focus(); }
  });
  var rb = $('#reset'); if (rb) rb.addEventListener('click', reset);
  $$('[data-level-go]').forEach(function (b) {
    b.addEventListener('click', function () { reset(); state.level = b.getAttribute('data-level-go'); apply(); toProjects(); });
  });
  $$('[data-filter-cat]').forEach(function (a) { a.addEventListener('click', function () { reset(); }); });
  $$('[data-cell-cat]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault(); reset();
      state.cat = a.getAttribute('data-cell-cat'); state.level = a.getAttribute('data-cell-level'); apply(); toProjects();
    });
  });

  /* Sorting and view */
  var sort = $('#sort');
  if (sort) sort.addEventListener('change', function () {
    blocks.forEach(function (b) {
      var g = b.querySelector('.grid');
      var items = Array.prototype.slice.call(g.children);
      items.sort(function (x, y) {
        return sort.value === 'name' ? x.dataset.name.localeCompare(y.dataset.name) : y.dataset.updated.localeCompare(x.dataset.updated);
      });
      items.forEach(function (i) { g.appendChild(i); });
    });
  });
  $$('.vbtn').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-view');
      $$('.vbtn').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (projects) projects.classList.toggle('compact', v === 'compact');
    });
  });

  /* Category menu */
  var t = $('#drawerToggle'), d = $('#drawer'), s = $('#drawerState');
  function setDrawer(open) {
    t.setAttribute('aria-checked', String(open));
    d.hidden = !open;
    if (s) s.textContent = open ? 'shown' : 'hidden';
  }
  if (t && d) {
    // On a narrow screen the menu starts closed, so the projects come first.
    if (window.matchMedia && window.matchMedia('(max-width: 760px)').matches) setDrawer(false);
    t.addEventListener('click', function () { setDrawer(t.getAttribute('aria-checked') !== 'true'); });
  }
  $$('.navmenu nav a').forEach(function (a) { a.addEventListener('click', function () { var m = $('.navmenu'); if (m) m.open = false; }); });

  /* Theme: follows the system until you choose; your choice is kept in this browser only */
  var th = $('#themeToggle');
  function isDark() {
    var set = root.getAttribute('data-theme');
    if (set) return set === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }
  if (th) {
    th.setAttribute('aria-checked', String(isDark()));
    th.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      th.setAttribute('aria-checked', String(next === 'dark'));
      try { localStorage.setItem('theme', next); } catch (x) { /* storage blocked: the choice lasts for this page only */ }
    });
  }

  /* Motion: counters and entrances, skipped under reduced motion */
  if (!reduced) {
    $$('.num[data-count]').forEach(function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10), t0 = null;
      el.textContent = '0';
      function step(ts) {
        if (t0 === null) t0 = ts;
        var k = Math.min(1, (ts - t0) / 1200);
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - k, 3))));
        if (k < 1) requestAnimationFrame(step); else el.textContent = String(target);
      }
      requestAnimationFrame(step);
    });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { var el = en.target; el.classList.add('in'); io.unobserve(el); setTimeout(function () { el.style.transitionDelay = ''; }, 900); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      $$('.featured, .way, .card, .wcard, .panel, .contact').forEach(function (el, i) {
        el.classList.add('reveal');
        el.style.transitionDelay = (i % 3) * 60 + 'ms';
        io.observe(el);
      });
    }
  }
  apply();
}());
