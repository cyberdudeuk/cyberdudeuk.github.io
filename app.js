/* Launchpad: filtering by area and level, sorting, and the drawer toggle. Everything works without this script. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var $$ = function (q) { return Array.prototype.slice.call(document.querySelectorAll(q)); };
  var cards = $$('.card'), blocks = $$('.cat-block'), cchips = $$('.cchip'), lchips = $$('.lchip');
  var shown = document.getElementById('shown');
  var state = { cat: 'all', level: 'all' };
  function apply() {
    cchips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-cat') === state.cat)); });
    lchips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-level') === state.level)); });
    var n = 0;
    blocks.forEach(function (b) {
      var any = false;
      b.querySelectorAll('.card').forEach(function (k) {
        var on = (state.cat === 'all' || k.dataset.category === state.cat) &&
                 (state.level === 'all' || (' ' + k.dataset.levels + ' ').indexOf(' ' + state.level + ' ') > -1);
        k.hidden = !on;
        if (on) { any = true; n += 1; }
      });
      b.hidden = !any;
    });
    if (shown) shown.textContent = n === cards.length ? 'Showing all ' + n + ' projects' : 'Showing ' + n + ' of ' + cards.length + ' projects';
  }
  cchips.forEach(function (c) { c.addEventListener('click', function () { state.cat = c.getAttribute('data-cat'); apply(); }); });
  lchips.forEach(function (c) { c.addEventListener('click', function () { state.level = c.getAttribute('data-level'); apply(); }); });
  $$('[data-level-go]').forEach(function (b) {
    b.addEventListener('click', function () {
      state.level = b.getAttribute('data-level-go'); state.cat = 'all'; apply();
      document.getElementById('projects').scrollIntoView();
    });
  });
  $$('[data-filter-cat]').forEach(function (a) { a.addEventListener('click', function () { state.cat = 'all'; state.level = 'all'; apply(); }); });
  var sort = document.getElementById('sort');
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
  var t = document.getElementById('drawerToggle'), d = document.getElementById('drawer'), s = document.getElementById('drawerState');
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
}());
