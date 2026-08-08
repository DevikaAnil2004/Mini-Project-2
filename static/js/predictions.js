/* CricketIQ — matchup simulator and player forecaster.
   Validation is inline and per-field; failures surface as a toast plus a
   field message rather than a blocking alert(). */

(function () {
  'use strict';

  var IQ = window.CricketIQ;
  var probabilityChart = null;

  function show(el) { if (el) el.classList.remove('is-hidden'); }
  function hide(el) { if (el) el.classList.add('is-hidden'); }

  /* On wide screens the result panel sits beside the form and is already in
     view; scrolling there would move the page for no reason. */
  function revealResult(el) {
    if (el && window.innerWidth < 1024) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function doughnutColours() {
    return [IQ.token('--series-1'), IQ.token('--series-2')];
  }

  /* ------------------------------------------------------------- matchup */

  function initMatchup() {
    var form = document.getElementById('predictionForm');
    if (!form) return;

    var teamA = document.getElementById('team1Select');
    var teamB = document.getElementById('team2Select');
    var button = document.getElementById('predictBtn');
    var placeholder = document.getElementById('placeholderCard');
    var results = document.getElementById('resultsCard');

    function validate() {
      var ok = true;

      IQ.setFieldError(form, 'team1', '');
      IQ.setFieldError(form, 'team2', '');

      if (!teamA.value) { IQ.setFieldError(form, 'team1', 'Pick a team.'); ok = false; }
      if (!teamB.value) { IQ.setFieldError(form, 'team2', 'Pick a second team.'); ok = false; }
      if (teamA.value && teamA.value === teamB.value) {
        IQ.setFieldError(form, 'team2', 'Pick a team other than ' + teamA.options[teamA.selectedIndex].text + '.');
        ok = false;
      }
      return ok;
    }

    teamA.addEventListener('change', function () { if (form.hasAttribute('data-submitted')) validate(); });
    teamB.addEventListener('change', function () { if (form.hasAttribute('data-submitted')) validate(); });

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      form.setAttribute('data-submitted', 'true');

      if (!validate()) {
        IQ.focusFirstInvalid(form);
        return;
      }

      var nameA = teamA.options[teamA.selectedIndex].getAttribute('data-name');
      var nameB = teamB.options[teamB.selectedIndex].getAttribute('data-name');

      IQ.setLoading(button, true);

      fetch('/api/predict/match?team1=' + encodeURIComponent(teamA.value) + '&team2=' + encodeURIComponent(teamB.value),
            { headers: { Accept: 'application/json' } })
        .then(function (response) { return response.json().then(function (body) { return { ok: response.ok, body: body }; }); })
        .then(function (result) {
          if (!result.ok || result.body.error) throw new Error(result.body.error || 'The prediction service did not respond.');
          render(result.body, nameA, nameB);
        })
        .catch(function (error) {
          IQ.toast(error.message, 'neg');
        })
        .finally(function () {
          IQ.setLoading(button, false);
        });
    });

    function render(data, nameA, nameB) {
      hide(placeholder);
      show(results);

      var probA = Number(data.team1.win_probability);
      var probB = Number(data.team2.win_probability);

      document.getElementById('team1NameResult').textContent = nameA;
      document.getElementById('team2NameResult').textContent = nameB;
      document.getElementById('team1ProbResult').textContent = probA + '%';
      document.getElementById('team2ProbResult').textContent = probB + '%';

      document.getElementById('probBarA').style.width = probA + '%';
      document.getElementById('probBarB').style.width = probB + '%';
      document.getElementById('probBar').setAttribute(
        'aria-label', nameA + ' ' + probA + ' percent, ' + nameB + ' ' + probB + ' percent'
      );

      var insight = document.getElementById('overallInsightResult').querySelector('span');
      insight.textContent = String(data.overall_insight || '')
        .replace(/\{team1\}/g, nameA)
        .replace(/\{team2\}/g, nameB);

      factors('team1FactorsTitle', 'team1FactorsList', nameA, data.team1.key_factors);
      factors('team2FactorsTitle', 'team2FactorsList', nameB, data.team2.key_factors);

      drawDoughnut(nameA, nameB, probA, probB);
      revealResult(results);
    }

    function factors(titleId, listId, name, items) {
      document.getElementById(titleId).textContent = name + ' factors';
      var list = document.getElementById(listId);
      list.innerHTML = '';

      (items || []).forEach(function (text) {
        var li = document.createElement('li');
        li.style.display = 'flex';
        li.style.gap = 'var(--s-2)';
        li.innerHTML =
          '<svg class="icon icon--sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" ' +
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="color: var(--pos-fg); margin-top:2px;">' +
          '<use href="#i-check"></use></svg><span></span>';
        li.querySelector('span').textContent = text;
        list.appendChild(li);
      });
    }

    function drawDoughnut(nameA, nameB, probA, probB) {
      var canvas = document.getElementById('probabilityChart');
      if (!canvas || typeof Chart === 'undefined') return;

      if (probabilityChart) probabilityChart.destroy();

      probabilityChart = new Chart(canvas.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: [nameA, nameB],
          datasets: [{
            data: [probA, probB],
            backgroundColor: doughnutColours(),
            borderColor: IQ.token('--surface'),
            borderWidth: 3,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '68%',
          animation: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? false : { duration: 420 },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: IQ.token('--surface-2'),
              titleColor: IQ.token('--ink'),
              bodyColor: IQ.token('--muted'),
              borderColor: IQ.token('--line-strong'),
              borderWidth: 1,
              cornerRadius: 8,
              callbacks: {
                label: function (context) { return context.label + ': ' + context.parsed + '%'; }
              }
            }
          }
        }
      });
    }

    IQ.onThemeChange(function () {
      if (!probabilityChart) return;
      probabilityChart.data.datasets[0].backgroundColor = doughnutColours();
      probabilityChart.data.datasets[0].borderColor = IQ.token('--surface');
      probabilityChart.options.plugins.tooltip.backgroundColor = IQ.token('--surface-2');
      probabilityChart.options.plugins.tooltip.titleColor = IQ.token('--ink');
      probabilityChart.options.plugins.tooltip.bodyColor = IQ.token('--muted');
      probabilityChart.update('none');
    });
  }

  /* ------------------------------------------------------------ forecaster */

  function initForecaster() {
    var form = document.getElementById('forecasterForm');
    if (!form) return;

    var select = document.getElementById('playerSelect');
    var button = document.getElementById('forecastBtn');
    var placeholder = document.getElementById('forecastPlaceholder');
    var results = document.getElementById('forecastResultsCard');

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      if (!select.value) {
        IQ.setFieldError(form, 'player', 'Pick a player.');
        IQ.focusFirstInvalid(form);
        return;
      }
      IQ.setFieldError(form, 'player', '');

      var playerName = select.options[select.selectedIndex].text;
      IQ.setLoading(button, true);

      fetch('/api/predict/player?player_id=' + encodeURIComponent(select.value), { headers: { Accept: 'application/json' } })
        .then(function (response) { return response.json().then(function (body) { return { ok: response.ok, body: body }; }); })
        .then(function (result) {
          if (!result.ok || result.body.error) throw new Error(result.body.error || 'The forecast service did not respond.');

          hide(placeholder);
          show(results);

          document.getElementById('forecastPlayerName').textContent = playerName;
          document.getElementById('predictedRuns').textContent = result.body.forecast;
          document.getElementById('recentForm').textContent =
            (result.body.recent_form && result.body.recent_form.length)
              ? result.body.recent_form.join('  ·  ')
              : 'No recorded innings';
          document.getElementById('confidenceResult').textContent = result.body.confidence || '—';
        })
        .catch(function (error) {
          IQ.toast(error.message, 'neg');
        })
        .finally(function () {
          IQ.setLoading(button, false);
        });
    });
  }

  function init() {
    if (!IQ) return;
    initMatchup();
    initForecaster();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
