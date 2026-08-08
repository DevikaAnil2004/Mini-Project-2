/* CricketIQ — analytics dashboard charts.
   Every colour is read from the CSS design tokens, so the charts re-theme
   with the rest of the interface instead of drifting to hard-coded hexes. */

(function () {
  'use strict';

  var IQ = window.CricketIQ;
  var charts = [];

  function theme() {
    return {
      ink: IQ.token('--ink'),
      muted: IQ.token('--muted'),
      faint: IQ.token('--faint'),
      line: IQ.token('--line'),
      surface: IQ.token('--surface-2'),
      border: IQ.token('--line-strong'),
      series: IQ.series()
    };
  }

  function baseOptions(t) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      animation: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? false : { duration: 420 },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: t.surface,
          titleColor: t.ink,
          bodyColor: t.muted,
          borderColor: t.border,
          borderWidth: 1,
          padding: 10,
          cornerRadius: 8,
          displayColors: true,
          boxPadding: 4
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          border: { display: false },
          grid: { color: t.line, drawTicks: false },
          ticks: { color: t.faint, padding: 8, font: { family: 'JetBrains Mono, monospace', size: 11 } }
        },
        x: {
          border: { display: false },
          grid: { display: false },
          ticks: { color: t.faint, padding: 6, font: { family: 'Inter, sans-serif', size: 11 } }
        }
      }
    };
  }

  function retheme() {
    var t = theme();
    charts.forEach(function (entry) {
      var chart = entry.chart;
      var fresh = baseOptions(t);
      chart.options.plugins.tooltip = fresh.plugins.tooltip;

      ['x', 'y'].forEach(function (axis) {
        var scale = chart.options.scales[axis];
        if (!scale) return;
        if (scale.grid && scale.grid.display !== false) scale.grid.color = t.line;
        if (scale.ticks) scale.ticks.color = t.faint;
        if (scale.title) scale.title.color = t.faint;
      });

      chart.data.datasets.forEach(function (dataset, i) {
        if (entry.kind === 'line') {
          var colour = t.series[i % t.series.length];
          dataset.borderColor = colour;
          dataset.backgroundColor = IQ.resolveColor('color-mix(in oklab, ' + colour + ' 16%, transparent)');
          dataset.pointBackgroundColor = colour;
          dataset.pointBorderColor = IQ.token('--surface');
        } else if (entry.colourToken) {
          dataset.backgroundColor = IQ.token(entry.colourToken);
        }
      });

      chart.update('none');
      if (entry.legend) buildLegend(entry);
    });
  }

  function chartFailure(frame, message) {
    frame.innerHTML =
      '<div class="empty empty--inline" style="height:100%; justify-content:center;">' +
      '<span class="empty__icon"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<use href="#i-alert-triangle"></use></svg></span>' +
      '<h3>Chart unavailable</h3><p></p></div>';
    frame.querySelector('p').textContent = message;
  }

  function clearSkeleton(frame) {
    var skeleton = frame.querySelector('[data-chart-skeleton]');
    if (skeleton) skeleton.remove();
  }

  function buildLegend(entry) {
    if (!entry.legend) return;
    entry.legend.innerHTML = '';

    entry.chart.data.datasets.forEach(function (dataset, index) {
      var button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('data-hidden', String(!entry.chart.isDatasetVisible(index)));
      button.setAttribute('aria-pressed', String(entry.chart.isDatasetVisible(index)));

      var swatch = document.createElement('span');
      swatch.className = 'swatch';
      swatch.style.background = dataset.borderColor || dataset.backgroundColor;

      var label = document.createElement('span');
      label.textContent = dataset.label;

      button.appendChild(swatch);
      button.appendChild(label);
      button.addEventListener('click', function () {
        var visible = entry.chart.isDatasetVisible(index);
        entry.chart.setDatasetVisibility(index, !visible);
        entry.chart.update();
        button.setAttribute('data-hidden', String(visible));
        button.setAttribute('aria-pressed', String(!visible));
      });

      entry.legend.appendChild(button);
    });
  }

  function loadTeamTrends() {
    var frame = document.querySelector('[data-chart="teamTrends"]');
    if (!frame) return;

    var canvas = document.getElementById('teamTrendsChart');
    var legend = document.querySelector('[data-chart-legend="teamTrends"]');
    var note = document.querySelector('[data-chart-note="teamTrends"]');
    var summary = document.querySelector('[data-chart-summary="teamTrends"]');

    fetch(frame.getAttribute('data-endpoint'), { headers: { Accept: 'application/json' } })
      .then(function (response) {
        if (!response.ok) throw new Error('Request failed (' + response.status + ')');
        return response.json();
      })
      .then(function (data) {
        if (data.error) throw new Error(data.error);

        var names = Object.keys(data);
        if (!names.length) {
          clearSkeleton(frame);
          chartFailure(frame, 'No season records have been loaded yet, so there is no trend to plot.');
          return;
        }

        var t = theme();
        var labels = data[names[0]].seasons;
        var longest = names.reduce(function (max, name) {
          return Math.max(max, data[name].seasons.length);
        }, 0);

        /* A line needs at least two points. With a single season on record,
           plot the final win counts as a ranked bar instead of an empty grid. */
        if (longest < 2) {
          clearSkeleton(frame);
          if (legend) legend.classList.add('is-hidden');

          var ranked = names.map(function (name) {
            return { name: name, wins: data[name].wins[0] || 0 };
          }).sort(function (a, b) { return b.wins - a.wins; });

          var single = baseOptions(t);
          single.indexAxis = 'y';
          single.interaction = { mode: 'nearest', intersect: true };
          single.scales.x.grid = { color: t.line, drawTicks: false };
          single.scales.x.ticks.stepSize = 1;
          single.scales.x.title = { display: true, text: 'Wins', color: t.faint };
          single.scales.y.grid = { display: false };
          single.scales.y.beginAtZero = false;
          single.scales.y.ticks.font = { family: 'Inter, sans-serif', size: 12 };

          charts.push({
            kind: 'bar',
            colourToken: '--series-1',
            chart: new Chart(canvas.getContext('2d'), {
              type: 'bar',
              data: {
                labels: ranked.map(function (r) { return r.name; }),
                datasets: [{
                  label: 'Wins',
                  data: ranked.map(function (r) { return r.wins; }),
                  backgroundColor: IQ.token('--series-1'),
                  borderRadius: 5,
                  borderSkipped: false,
                  barThickness: 20
                }]
              },
              options: single
            })
          });

          var subtitle = document.querySelector('[data-chart-subtitle="teamTrends"]');
          if (subtitle) subtitle.textContent = 'Season ' + labels[0] + ', ranked';

          if (note) {
            note.classList.remove('is-hidden');
            note.textContent = 'Only season ' + labels[0] + ' is on record, so this ranks final win counts ' +
              'rather than plotting a trend. Load more seasons to see movement over time.';
          }
          if (summary) {
            summary.textContent = 'Final win counts for ' + ranked.length + ' franchises in season ' + labels[0] + '.';
          }
          return;
        }

        var datasets = names.map(function (name, i) {
          var colour = t.series[i % t.series.length];
          return {
            label: name,
            data: data[name].wins,
            borderColor: colour,
            backgroundColor: IQ.resolveColor('color-mix(in oklab, ' + colour + ' 16%, transparent)'),
            pointBackgroundColor: colour,
            pointBorderColor: IQ.token('--surface'),
            pointBorderWidth: 2,
            pointRadius: 3,
            pointHoverRadius: 6,
            borderWidth: 2,
            tension: 0.35,
            fill: false
          };
        });

        clearSkeleton(frame);

        var options = baseOptions(t);
        options.scales.y.ticks.stepSize = 1;
        options.scales.y.title = { display: true, text: 'Wins', color: t.faint };
        options.scales.x.title = { display: true, text: 'Season', color: t.faint };

        var entry = {
          kind: 'line',
          legend: legend,
          chart: new Chart(canvas.getContext('2d'), { type: 'line', data: { labels: labels, datasets: datasets }, options: options })
        };
        charts.push(entry);
        buildLegend(entry);

        if (summary) {
          summary.textContent = 'Wins per season for ' + names.length + ' franchises across seasons ' +
            labels[0] + ' to ' + labels[labels.length - 1] + '.';
        }
      })
      .catch(function (error) {
        clearSkeleton(frame);
        chartFailure(frame, 'Could not load season trends. ' + error.message);
      });
  }

  /* Published IPL career totals — flagged as such in the page copy. */
  var LEADERS = {
    runs: {
      labels: ['V Kohli', 'S Dhawan', 'D Warner', 'R Sharma', 'S Raina'],
      values: [7263, 6617, 6397, 6211, 5528],
      axis: 'Runs'
    },
    wickets: {
      labels: ['Y Chahal', 'D Bravo', 'P Chawla', 'A Mishra', 'R Ashwin'],
      values: [187, 183, 179, 173, 171],
      axis: 'Wickets'
    }
  };

  function leaderboard(canvasId, config, colourToken) {
    var canvas = document.getElementById(canvasId);
    if (!canvas) return;

    var t = theme();
    var options = baseOptions(t);
    options.indexAxis = 'y';
    options.interaction = { mode: 'nearest', intersect: true };
    options.scales.x.grid = { color: t.line, drawTicks: false };
    options.scales.x.title = { display: true, text: config.axis, color: t.faint };
    options.scales.y.grid = { display: false };
    options.scales.y.beginAtZero = false;
    options.scales.y.ticks.font = { family: 'Inter, sans-serif', size: 12 };

    var entry = {
      kind: 'bar',
      colourToken: colourToken,
      chart: new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: config.labels,
          datasets: [{
            label: config.axis,
            data: config.values,
            backgroundColor: IQ.token(colourToken),
            borderRadius: 5,
            borderSkipped: false,
            barThickness: 20
          }]
        },
        options: options
      })
    };
    charts.push(entry);
  }

  function init() {
    if (typeof Chart === 'undefined' || !IQ) return;

    Chart.defaults.font.family = 'Inter, system-ui, sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.color = IQ.token('--muted');

    loadTeamTrends();
    leaderboard('topScorersChart', LEADERS.runs, '--series-1');
    leaderboard('topWicketsChart', LEADERS.wickets, '--series-5');

    IQ.onThemeChange(retheme);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
