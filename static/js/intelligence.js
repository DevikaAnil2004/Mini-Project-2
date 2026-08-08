/* CricketIQ — selection assistant and player similarity.
   Both panes share the same shape: validate inline, load with a busy button,
   then swap the placeholder for a result panel. */

(function () {
  'use strict';

  var IQ = window.CricketIQ;

  function show(el) { if (el) el.classList.remove('is-hidden'); }
  function hide(el) { if (el) el.classList.add('is-hidden'); }

  /* On wide screens the result panel sits beside the form and is already in
     view; scrolling there would move the page for no reason. */
  function revealResult(el) {
    if (el && window.innerWidth < 1024) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function readJson(response) {
    return response.json().then(function (body) { return { ok: response.ok, body: body }; });
  }

  function roleBadge(role) {
    var tone = { 'Batsman': 'accent', 'Bowler': 'info', 'All-rounder': 'pos', 'Wicket-keeper': 'warn' }[role];
    var span = document.createElement('span');
    span.className = 'badge-pill' + (tone ? ' badge-pill--' + tone : '');
    span.textContent = role || 'Unassigned';
    return span;
  }

  function cell(row, content) {
    var td = document.createElement('td');
    if (content instanceof Node) td.appendChild(content);
    else td.textContent = content;
    row.appendChild(td);
    return td;
  }

  /* ------------------------------------------------- selection assistant */

  function initAssistant() {
    var form = document.getElementById('assistantForm');
    if (!form) return;

    var team = document.getElementById('teamSelect');
    var opponent = document.getElementById('oppSelect');
    var button = document.getElementById('assistBtn');
    var placeholder = document.getElementById('placeholderCard');
    var results = document.getElementById('resultsCard');
    var list = document.getElementById('xiList');

    function validate() {
      var ok = true;
      IQ.setFieldError(form, 'team', '');
      IQ.setFieldError(form, 'opponent', '');

      if (!team.value) { IQ.setFieldError(form, 'team', 'Pick your team.'); ok = false; }
      if (!opponent.value) { IQ.setFieldError(form, 'opponent', 'Pick an opponent.'); ok = false; }
      if (team.value && team.value === opponent.value) {
        IQ.setFieldError(form, 'opponent', 'A team cannot play itself — pick a different opponent.');
        ok = false;
      }
      return ok;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!validate()) { IQ.focusFirstInvalid(form); return; }

      IQ.setLoading(button, true);

      fetch('/api/assistant/team_selection?team_id=' + encodeURIComponent(team.value) +
            '&opponent_id=' + encodeURIComponent(opponent.value), { headers: { Accept: 'application/json' } })
        .then(readJson)
        .then(function (result) {
          if (!result.ok || result.body.error) throw new Error(result.body.error || 'The assistant did not respond.');

          hide(placeholder);
          show(results);

          document.getElementById('reasoningResult').querySelector('span').textContent = result.body.reasoning;

          list.innerHTML = '';
          (result.body.suggested_xi || []).forEach(function (player, index) {
            var row = document.createElement('tr');
            cell(row, String(index + 1)).className = 'num';
            cell(row, player.name).className = 'primary-cell';
            cell(row, roleBadge(player.role));
            list.appendChild(row);
          });

          revealResult(results);
        })
        .catch(function (error) { IQ.toast(error.message, 'neg'); })
        .finally(function () { IQ.setLoading(button, false); });
    });
  }

  /* ------------------------------------------------------------ similarity */

  function initSimilarity() {
    var form = document.getElementById('similarityForm');
    if (!form) return;

    var select = document.getElementById('playerSelect');
    var button = document.getElementById('simBtn');
    var placeholder = document.getElementById('placeholderCard');
    var results = document.getElementById('resultsCard');
    var list = document.getElementById('simList');

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      if (!select.value) {
        IQ.setFieldError(form, 'player', 'Pick a player.');
        IQ.focusFirstInvalid(form);
        return;
      }
      IQ.setFieldError(form, 'player', '');

      IQ.setLoading(button, true);

      fetch('/api/players/similarity?player_id=' + encodeURIComponent(select.value), { headers: { Accept: 'application/json' } })
        .then(readJson)
        .then(function (result) {
          if (!result.ok || result.body.error) throw new Error(result.body.error || 'The clustering service did not respond.');

          hide(placeholder);
          show(results);

          document.getElementById('clusterBadge').textContent = 'Cluster ' + result.body.cluster_id;

          list.innerHTML = '';
          var similar = result.body.similar_players || [];

          if (!similar.length) {
            var row = document.createElement('tr');
            var td = document.createElement('td');
            td.colSpan = 3;
            td.style.color = 'var(--muted)';
            td.textContent = 'No other player falls in this cluster.';
            row.appendChild(td);
            list.appendChild(row);
          } else {
            similar.forEach(function (player) {
              var row = document.createElement('tr');
              cell(row, player.name).className = 'primary-cell';
              cell(row, player.team || '—');
              cell(row, roleBadge(player.role));
              list.appendChild(row);
            });
          }

          revealResult(results);
        })
        .catch(function (error) { IQ.toast(error.message, 'neg'); })
        .finally(function () { IQ.setLoading(button, false); });
    });
  }

  function init() {
    if (!IQ) return;
    initAssistant();
    initSimilarity();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
