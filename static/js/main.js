/* CricketIQ — shell behaviour.
   Theme, navigation drawer, toasts, live table filtering, column sorting and
   the token bridge that keeps Chart.js in step with the CSS design tokens.
   No dependencies. */

(function () {
  'use strict';

  var THEME_KEY = 'cricketiq-theme';
  var root = document.documentElement;

  /* ---------------------------------------------------------------- tokens */

  /* Colours live in CSS. This probe resolves any CSS colour expression
     (including var() and color-mix()) to a concrete value the canvas can
     paint, so charts never hard-code a hex that drifts from the stylesheet. */
  var probe = document.createElement('span');
  probe.setAttribute('aria-hidden', 'true');
  probe.style.cssText = 'position:absolute;width:0;height:0;visibility:hidden;pointer-events:none';

  function resolveColor(expression) {
    if (!probe.isConnected) document.body.appendChild(probe);
    probe.style.color = '';
    probe.style.color = expression;
    return getComputedStyle(probe).color;
  }

  function token(name) {
    return resolveColor('var(' + name + ')');
  }

  function alpha(name, amount) {
    return resolveColor('color-mix(in oklab, var(' + name + ') ' + Math.round(amount * 100) + '%, transparent)');
  }

  function series() {
    var out = [];
    for (var i = 1; i <= 8; i++) out.push(token('--series-' + i));
    return out;
  }

  /* ----------------------------------------------------------------- theme */

  function currentTheme() {
    return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);

    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      btn.querySelectorAll('[data-theme-icon]').forEach(function (span) {
        span.hidden = span.getAttribute('data-theme-icon') !== theme;
      });
    });

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#141518' : '#f7f7f9');

    document.dispatchEvent(new CustomEvent('cricketiq:themechange', { detail: { theme: theme } }));
  }

  function initTheme() {
    applyTheme(currentTheme());

    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = currentTheme() === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* private mode */ }
        applyTheme(next);
      });
    });

  }

  /* ------------------------------------------------------------ navigation */

  function initNav() {
    var sidebar = document.querySelector('[data-sidebar]');
    var scrim = document.querySelector('[data-scrim]');
    var opener = document.querySelector('[data-open-nav]');
    if (!sidebar || !scrim || !opener) return;

    var isOpen = false;

    function setOpen(open) {
      isOpen = open;
      sidebar.setAttribute('data-open', String(open));
      scrim.setAttribute('data-open', String(open));
      scrim.hidden = !open;
      opener.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';

      if (open) {
        var closer = sidebar.querySelector('[data-close-nav]');
        if (closer) closer.focus();
      } else {
        opener.focus();
      }
    }

    opener.addEventListener('click', function () { setOpen(true); });
    scrim.addEventListener('click', function () { setOpen(false); });

    sidebar.querySelectorAll('[data-close-nav]').forEach(function (btn) {
      btn.addEventListener('click', function () { setOpen(false); });
    });

    /* A tap on any destination should dismiss the drawer, not leave it hanging. */
    sidebar.querySelectorAll('a[href]').forEach(function (link) {
      link.addEventListener('click', function () { if (isOpen) setOpen(false); });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen) setOpen(false);
    });

    /* Crossing into the desktop layout leaves the drawer state behind. */
    var desktop = window.matchMedia('(min-width: 1200px)');
    var onBreakpoint = function (event) {
      if (event.matches && isOpen) {
        isOpen = false;
        sidebar.setAttribute('data-open', 'false');
        scrim.setAttribute('data-open', 'false');
        scrim.hidden = true;
        opener.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    };
    if (desktop.addEventListener) desktop.addEventListener('change', onBreakpoint);
    else if (desktop.addListener) desktop.addListener(onBreakpoint);
  }

  /* ---------------------------------------------------------------- toasts */

  var ICONS = { pos: 'check-circle', neg: 'alert-circle', info: 'info' };

  function toast(message, tone, timeout) {
    var region = document.querySelector('[data-toast-region]');
    if (!region) return;

    tone = ICONS[tone] ? tone : 'info';

    var el = document.createElement('div');
    el.className = 'toast toast--' + tone;
    el.setAttribute('role', tone === 'neg' ? 'alert' : 'status');
    el.innerHTML =
      '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><use href="#i-' + ICONS[tone] + '"></use></svg>' +
      '<span class="toast__msg"></span>' +
      '<button type="button" class="toast__close" aria-label="Dismiss notification">' +
      '<svg class="icon icon--sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><use href="#i-x"></use></svg></button>';
    el.querySelector('.toast__msg').textContent = message;

    function dismiss() {
      el.setAttribute('data-leaving', 'true');
      window.setTimeout(function () { el.remove(); }, 200);
    }

    el.querySelector('.toast__close').addEventListener('click', dismiss);
    region.appendChild(el);
    window.setTimeout(dismiss, timeout || 5000);
  }

  /* ---------------------------------------------------------- live filters */

  function initFilters() {
    document.querySelectorAll('[data-filter-input]').forEach(function (input) {
      var key = input.getAttribute('data-filter-input');
      var container = document.querySelector('[data-filter-target="' + key + '"]');
      var emptyState = document.querySelector('[data-filter-empty="' + key + '"]');
      if (!container) return;

      var rows = Array.prototype.slice.call(container.querySelectorAll('[data-filter-text]'));
      /* For tables the filter target is the tbody, so hide the whole panel
         rather than leaving a header row floating above nothing. */
      var hideTarget = container.closest('.panel') || container;
      var timer = null;

      function run() {
        var needle = input.value.trim().toLowerCase();
        var visible = 0;

        rows.forEach(function (row) {
          var match = !needle || row.getAttribute('data-filter-text').toLowerCase().indexOf(needle) !== -1;
          row.hidden = !match;
          if (match) visible++;
        });

        if (emptyState) emptyState.hidden = visible !== 0;
        hideTarget.hidden = visible === 0 && rows.length > 0;
      }

      input.addEventListener('input', function () {
        window.clearTimeout(timer);
        timer = window.setTimeout(run, 120);
      });
    });
  }

  /* ------------------------------------------------------------ table sort */

  function cellValue(row, index, kind) {
    var cell = row.children[index];
    var text = cell ? cell.textContent.trim() : '';
    if (kind === 'number') {
      var n = parseFloat(text.replace(/[^0-9.\-]/g, ''));
      return isNaN(n) ? -Infinity : n;
    }
    return text.toLowerCase();
  }

  function initSortableTables() {
    document.querySelectorAll('table[data-sortable]').forEach(function (table) {
      var body = table.tBodies[0];
      if (!body) return;

      table.querySelectorAll('th[data-sort]').forEach(function (th) {
        var index = Array.prototype.indexOf.call(th.parentNode.children, th);
        var kind = th.getAttribute('data-sort');

        th.setAttribute('tabindex', '0');
        th.setAttribute('role', 'columnheader');
        th.setAttribute('aria-sort', 'none');

        function sort() {
          var ascending = th.getAttribute('aria-sort') !== 'ascending';

          table.querySelectorAll('th[data-sort]').forEach(function (other) {
            other.setAttribute('aria-sort', 'none');
          });
          th.setAttribute('aria-sort', ascending ? 'ascending' : 'descending');

          var rows = Array.prototype.slice.call(body.rows);
          rows.sort(function (a, b) {
            var av = cellValue(a, index, kind);
            var bv = cellValue(b, index, kind);
            if (av < bv) return ascending ? -1 : 1;
            if (av > bv) return ascending ? 1 : -1;
            return 0;
          });

          var fragment = document.createDocumentFragment();
          rows.forEach(function (row) { fragment.appendChild(row); });
          body.appendChild(fragment);
        }

        th.addEventListener('click', sort);
        th.addEventListener('keydown', function (event) {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            sort();
          }
        });
      });
    });
  }

  /* ------------------------------------------------------------------ init */

  function init() {
    initTheme();
    initNav();
    initFilters();
    initSortableTables();
  }

  /* ------------------------------------------------- form state utilities */

  /* Errors sit next to the field they belong to and are announced, rather
     than being thrown at the user in a blocking alert(). */
  function setFieldError(form, fieldName, message) {
    var field = form.querySelector('[data-field="' + fieldName + '"]');
    if (!field) return;

    if (message) {
      field.setAttribute('data-invalid', 'true');
      var slot = field.querySelector('[data-error] span');
      if (slot) slot.textContent = message;
      var control = field.querySelector('.input, .select');
      if (control) control.setAttribute('aria-invalid', 'true');
    } else {
      field.removeAttribute('data-invalid');
      var ok = field.querySelector('.input, .select');
      if (ok) ok.removeAttribute('aria-invalid');
    }
  }

  function focusFirstInvalid(form) {
    var field = form.querySelector('[data-invalid="true"] .input, [data-invalid="true"] .select');
    if (field) field.focus();
  }

  function setLoading(button, loading) {
    button.setAttribute('data-loading', String(loading));
    button.disabled = loading;
    button.setAttribute('aria-busy', String(loading));
  }

  window.CricketIQ = {
    toast: toast,
    setFieldError: setFieldError,
    focusFirstInvalid: focusFirstInvalid,
    setLoading: setLoading,
    token: token,
    alpha: alpha,
    series: series,
    resolveColor: resolveColor,
    onThemeChange: function (handler) {
      document.addEventListener('cricketiq:themechange', function (e) { handler(e.detail.theme); });
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
