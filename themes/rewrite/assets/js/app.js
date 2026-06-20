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

  /* ---- Homepage showcase carousel ----
   * Ported from the legacy explore.html partial.  DOM structure
   * (.showcase-wrapper / .showcase-item.active / .showcase-dots /
   * .showcase-prev|next|pause / .showcase-progress-bar) is
   * preserved 1:1 so behaviour matches the original. */
  var showcaseWrapper = document.querySelector('.showcase-wrapper');
  var showcaseItems   = document.querySelectorAll('.showcase-item');
  var dotsContainer   = document.querySelector('.showcase-dots');
  var progressBar     = document.querySelector('.showcase-progress-bar');
  var prevBtn         = document.querySelector('.showcase-prev');
  var nextBtn         = document.querySelector('.showcase-next');
  var pauseBtn        = document.querySelector('.showcase-pause');

  if (showcaseWrapper && showcaseItems.length > 0) {
    var currentIndex = 0;
    var isPaused = false;
    var intervalId = null;
    var progressIntervalId = null;
    var INTERVAL_DURATION = 8000;
    var PROGRESS_UPDATE_INTERVAL = 50;
    var progressValue = 0;

    // Build dots for each slide
    if (dotsContainer) {
      showcaseItems.forEach(function (item, index) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'showcase-dot' + (index === 0 ? ' active' : '');
        dot.setAttribute('data-index', index);
        dot.setAttribute('aria-label', 'Go to slide ' + (index + 1));
        dot.addEventListener('click', function () { goToSlide(index); });
        dotsContainer.appendChild(dot);
      });
    }
    var dots = document.querySelectorAll('.showcase-dot');

    function goToSlide(index) {
      showcaseItems[currentIndex].classList.remove('active');
      if (dots[currentIndex]) dots[currentIndex].classList.remove('active');
      currentIndex = (index + showcaseItems.length) % showcaseItems.length;
      showcaseItems[currentIndex].classList.add('active');
      if (dots[currentIndex]) dots[currentIndex].classList.add('active');
      resetProgress();
    }
    function nextSlide() { goToSlide(currentIndex + 1); }
    function prevSlide() { goToSlide(currentIndex - 1); }

    function resetProgress() {
      progressValue = 0;
      if (progressBar) progressBar.style.width = '0%';
    }
    function updateProgress() {
      if (isPaused || !progressBar) return;
      progressValue += (PROGRESS_UPDATE_INTERVAL / INTERVAL_DURATION) * 100;
      progressBar.style.width = Math.min(progressValue, 100) + '%';
    }

    function startAutoplay() {
      stopAutoplay();
      intervalId = setInterval(function () { if (!isPaused) nextSlide(); }, INTERVAL_DURATION);
      progressIntervalId = setInterval(updateProgress, PROGRESS_UPDATE_INTERVAL);
    }
    function stopAutoplay() {
      if (intervalId)         { clearInterval(intervalId);         intervalId = null; }
      if (progressIntervalId) { clearInterval(progressIntervalId); progressIntervalId = null; }
    }

    function togglePause() {
      isPaused = !isPaused;
      if (pauseBtn) {
        pauseBtn.classList.toggle('paused', isPaused);
        pauseBtn.setAttribute('aria-label', isPaused ? 'Resume autoplay' : 'Pause autoplay');
        var lbl = pauseBtn.querySelector('span');
        if (lbl) lbl.textContent = isPaused ? '▶' : '⏸';
      }
      if (!isPaused) startAutoplay();
    }

    if (prevBtn)  prevBtn.addEventListener('click',  function () { prevSlide(); });
    if (nextBtn)  nextBtn.addEventListener('click',  function () { nextSlide(); });
    if (pauseBtn) pauseBtn.addEventListener('click', togglePause);

    // Pause on hover
    showcaseWrapper.addEventListener('mouseenter', stopAutoplay);
    showcaseWrapper.addEventListener('mouseleave', function () { if (!isPaused) startAutoplay(); });

    // Touch swipe
    var touchStartX = 0, touchEndX = 0;
    showcaseWrapper.addEventListener('touchstart', function (e) {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    showcaseWrapper.addEventListener('touchend', function (e) {
      touchEndX = e.changedTouches[0].screenX;
      var diff = touchStartX - touchEndX;
      if (Math.abs(diff) > 50) { if (diff > 0) nextSlide(); else prevSlide(); }
    }, { passive: true });

    // Keyboard arrows (when carousel is in viewport)
    document.addEventListener('keydown', function (e) {
      var rect = showcaseWrapper.getBoundingClientRect();
      if (rect.top >= window.innerHeight || rect.bottom <= 0) return;
      if      (e.key === 'ArrowLeft')  prevSlide();
      else if (e.key === 'ArrowRight') nextSlide();
    });

    // Honour prefers-reduced-motion: only start autoplay if user is OK with motion
    var mql = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (!mql.matches) startAutoplay();
  }

})();
