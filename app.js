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
      try { localStorage.setItem('theme', next); } catch { /* storage blocked: the choice lasts for this page only */ }
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
      $$('.spotlight, .door, .way, .card, .wcard, .panel, .contact').forEach(function (el, i) {
        el.classList.add('reveal');
        el.style.transitionDelay = (i % 3) * 60 + 'ms';
        io.observe(el);
      });
    }
  }
  /* Masthead (D-33): the section links fold into the menu whenever they would wrap, whatever the font or text size.
     The CSS fold point is the fallback without JavaScript. */
  var navg = $('nav.global'), themeBtn = $('#themeToggle');
  if (navg && themeBtn) {
    var fit = function () {
      root.classList.remove('nav-fold');
      if (getComputedStyle(navg).display === 'none') return;
      var a = navg.getBoundingClientRect(), t = themeBtn.getBoundingClientRect();
      if (Math.abs((a.top + a.bottom) / 2 - (t.top + t.bottom) / 2) > 8 || a.right > window.innerWidth) root.classList.add('nav-fold');
    };
    window.addEventListener('resize', fit);
    window.addEventListener('load', fit);
    if (document.fonts) {
      if (document.fonts.ready) document.fonts.ready.then(fit);
      if (document.fonts.addEventListener) document.fonts.addEventListener('loadingdone', fit);
    }
    fit();
  }

  /* Spotlight carousel (D-29): previous, next and dots move the strip; it rotates only when the reader presses Play,
     never under reduced motion, and pauses while the pointer or keyboard focus is inside it (WCAG 2.2.2). */
  var strack = $('#spotTrack');
  if (strack) {
    var slides = $$('#spotTrack .slide'), sdots = $$('.sdot'), play = $('#spotPlay'), timer = null, held = false;
    var cur = function () { return Math.round(strack.scrollLeft / Math.max(1, strack.clientWidth)); };
    var go = function (i) {
      var n = (i + slides.length) % slides.length;
      strack.scrollTo({ left: slides[n].offsetLeft - slides[0].offsetLeft, behavior: reduced ? 'auto' : 'smooth' });
    };
    var mark = function () {
      var i = cur();
      sdots.forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
      slides.forEach(function (sl, k) { sl.setAttribute('aria-hidden', String(k !== i)); sl.inert = k !== i; });
    };
    var stop = function () { if (timer) { clearInterval(timer); timer = null; } };
    var start = function () { stop(); timer = setInterval(function () { if (!held) go(cur() + 1); }, 7000); };
    var setPlay = function (on) {
      if (!play) return;
      play.setAttribute('aria-pressed', String(on));
      play.textContent = on ? 'Pause' : 'Play';
      strack.setAttribute('aria-live', on ? 'off' : 'polite');
      if (on) start(); else stop();
    };
    var st = null;
    strack.addEventListener('scroll', function () { clearTimeout(st); st = setTimeout(mark, 80); }, { passive: true });
    $('#spotPrev').addEventListener('click', function () { go(cur() - 1); });
    $('#spotNext').addEventListener('click', function () { go(cur() + 1); });
    sdots.forEach(function (d) { d.addEventListener('click', function () { go(Number(d.getAttribute('data-slide'))); }); });
    strack.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowRight') { ev.preventDefault(); go(cur() + 1); } else if (ev.key === 'ArrowLeft') { ev.preventDefault(); go(cur() - 1); }
    });
    var area = strack;
    area.addEventListener('pointerenter', function () { held = true; });
    area.addEventListener('pointerleave', function () { held = false; });
    area.addEventListener('focusin', function () { held = true; });
    area.addEventListener('focusout', function () { held = false; });
    if (play) play.addEventListener('click', function () { setPlay(play.getAttribute('aria-pressed') !== 'true'); });
    if (reduced && play) play.hidden = true;
    mark();
  }

  /* Back to top: appears after the first screen; its ring shows how far down the page you are */
  var top = $('#toTop'), topRing = $('#toTopRing');
  if (top) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var k = h > 0 ? Math.min(1, window.scrollY / h) : 0;
      top.classList.toggle('show', window.scrollY > 600);
      if (topRing) topRing.style.strokeDashoffset = String(144.5 * (1 - k));
    };
    window.addEventListener('scroll', tick, { passive: true });
    tick();
    top.addEventListener('click', function (ev) {
      ev.preventDefault();
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
      var h1 = $('#top'); if (h1) h1.setAttribute('tabindex', '-1');
      setTimeout(function () { if (h1) h1.focus({ preventScroll: true }); }, reduced ? 0 : 600);
    });
  }

  /* Sections mark themselves seen, so their heading icon draws in and charts grow (CSS does the rest) */
  if ('IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('seen'); so.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -15% 0px' });
    $$('main > section').forEach(function (s2) { so.observe(s2); });
  } else {
    $$('main > section').forEach(function (s2) { s2.classList.add('seen'); });
  }

  /* Pointer effects: a spotlight on cards and a gentle parallax on the hero illustration. Fine pointers only, never
     under reduced motion. */
  var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (fine && !reduced) {
    $$('.card, .wcard, .way').forEach(function (el) {
      el.addEventListener('pointermove', function (ev) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (ev.clientX - r.left) + 'px');
        el.style.setProperty('--my', (ev.clientY - r.top) + 'px');
      });
    });
    var hero = $('#top'), art = $('.hero-art .constellation');
    if (hero && art) {
      hero.addEventListener('pointermove', function (ev) {
        var r = hero.getBoundingClientRect();
        var x = (ev.clientX - r.left) / r.width - .5, y = (ev.clientY - r.top) / r.height - .5;
        art.style.transform = 'translate(' + (x * 14).toFixed(1) + 'px,' + (y * 10).toFixed(1) + 'px)';
      });
      hero.addEventListener('pointerleave', function () { art.style.transform = ''; });
    }
  }
  apply();
}());
