/* ============================================================
 *  Rewrite — minimal JS.
 *  Only what can't be done declaratively: mobile nav toggle,
 *  colour-scheme persistence, external-link safety.
 * ============================================================ */

(function () {
  'use strict';

  /* ---- Mobile nav toggle ---- */
  var nav    = document.querySelector('.primary-nav');
  var toggle = nav && nav.querySelector('.primary-nav__toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
    });
    document.addEventListener('click', function (e) {
      if (nav.getAttribute('data-open') === 'true' && !nav.contains(e.target)) {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---- Colour-scheme persistence (light / dark / auto) ----
   * Read at the earliest moment in <head> via the inline script
   * below; this listener handles explicit toggles, if a button
   * with [data-toggle="color-scheme"] is added to the page. */
  try {
    var STORE = 'kartoza-color-scheme';
    var saved = localStorage.getItem(STORE);
    if (saved) document.documentElement.setAttribute('data-color-scheme', saved);
    document.querySelectorAll('[data-toggle="color-scheme"]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-color-scheme');
        var next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-color-scheme', next);
        localStorage.setItem(STORE, next);
      });
    });
  } catch (e) { /* localStorage unavailable */ }

  /* ---- External link safety: add rel + target where missing ---- */
  var origin = location.origin;
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.href.indexOf(origin) === 0) return;
    if (!a.hasAttribute('rel'))    a.setAttribute('rel', 'noopener noreferrer');
    if (!a.hasAttribute('target')) a.setAttribute('target', '_blank');
  });

})();
