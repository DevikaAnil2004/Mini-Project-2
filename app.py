import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify
from sqlalchemy import distinct, func
from sqlalchemy.orm import joinedload, selectinload

from config import config
from models import db, Team, Player, Match, BattingStatistic, BowlingStatistic, TeamStatistic

app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Static assets carry no fingerprint, so cache them only when debug is off —
# otherwise edits to CSS/JS appear to do nothing during development.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = (
    timedelta(0) if app.config.get('DEBUG') else timedelta(hours=12)
)

# Initialize extensions
db.init_app(app)


@app.context_processor
def inject_globals():
    """Values every template needs."""
    return {'current_year': datetime.now().year}


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


def _dashboard_stats():
    """Counts for the overview tiles, in one pass per table."""
    return {
        'total_teams': db.session.query(func.count(Team.id)).scalar() or 0,
        'total_players': db.session.query(func.count(Player.id)).scalar() or 0,
        'total_matches': db.session.query(func.count(Match.id)).scalar() or 0,
        'completed_matches': db.session.query(func.count(Match.id))
                                       .filter(Match.status == 'completed').scalar() or 0,
        'total_seasons': db.session.query(func.count(distinct(TeamStatistic.season))).scalar() or 0,
    }


# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    try:
        latest_matches = (Match.query
                          .options(joinedload(Match.home_team_obj), joinedload(Match.away_team_obj))
                          .order_by(Match.match_date.desc())
                          .limit(5)
                          .all())
        return render_template('index.html', stats=_dashboard_stats(), latest_matches=latest_matches)
    except Exception as e:
        app.logger.exception('Error on index route: %s', e)
        return render_template('index.html', stats={}, latest_matches=[])


@app.route('/teams')
def teams():
    """Teams listing page"""
    try:
        page = request.args.get('page', 1, type=int)
        # selectinload keeps the "N players" badge from firing one query per card.
        teams_list = (Team.query
                      .options(selectinload(Team.players))
                      .order_by(Team.name)
                      .paginate(page=page, per_page=20, error_out=False))
        return render_template('teams/index.html', teams=teams_list.items, pagination=teams_list)
    except Exception as e:
        app.logger.exception('Error on teams route: %s', e)
        return render_template('teams/index.html', teams=[], pagination=None)


@app.route('/teams/<int:team_id>')
def team_detail(team_id):
    """Team detail page"""
    team = Team.query.get_or_404(team_id)
    players = (Player.query
               .filter_by(team_id=team_id, is_active=True)
               .order_by(Player.name)
               .all())
    stats = (TeamStatistic.query
             .filter_by(team_id=team_id)
             .order_by(TeamStatistic.season.desc())
             .first())
    return render_template('teams/detail.html', team=team, players=players, stats=stats)


@app.route('/players')
def players():
    """Players listing page with role, team and search filters"""
    roles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper']
    try:
        role_filter = request.args.get('role', '').strip()
        search_query = request.args.get('q', '').strip()
        team_filter = request.args.get('team', type=int)
        page = request.args.get('page', 1, type=int)

        query = Player.query.options(joinedload(Player.team)).filter_by(is_active=True)
        if role_filter in roles:
            query = query.filter_by(role=role_filter)
        else:
            role_filter = ''

        if team_filter:
            query = query.filter_by(team_id=team_filter)

        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                (Player.name.ilike(search_pattern)) |
                (Player.country.ilike(search_pattern))
            )

        players_list = query.order_by(Player.name).paginate(page=page, per_page=24, error_out=False)
        all_teams = Team.query.order_by(Team.name).all()

        return render_template('players/index.html',
                               players=players_list.items,
                               pagination=players_list,
                               roles=roles,
                               teams=all_teams,
                               selected_role=role_filter,
                               selected_team=team_filter,
                               search_query=search_query)
    except Exception as e:
        app.logger.exception('Error on players route: %s', e)
        return render_template('players/index.html',
                               players=[], pagination=None, roles=roles, teams=[],
                               selected_role='', selected_team=None, search_query='')


@app.route('/players/<int:player_id>')
def player_detail(player_id):
    """Player detail page"""
    player = Player.query.options(joinedload(Player.team)).get_or_404(player_id)

    batting_stats = (BattingStatistic.query
                     .filter_by(player_id=player_id)
                     .order_by(BattingStatistic.match_id.desc())
                     .all())
    bowling_stats = (BowlingStatistic.query
                     .filter_by(player_id=player_id)
                     .order_by(BowlingStatistic.match_id.desc())
                     .all())

    # A player who batted and bowled in the same fixture played one match,
    # not two — count distinct fixtures.
    match_ids = {s.match_id for s in batting_stats} | {s.match_id for s in bowling_stats}

    total_runs = sum(s.runs or 0 for s in batting_stats)
    balls_faced = sum(s.balls_faced or 0 for s in batting_stats)
    runs_conceded = sum(s.runs_conceded or 0 for s in bowling_stats)
    # Comprehensive career aggregates
    fours = sum(s.fours or 0 for s in batting_stats)
    sixes = sum(s.sixes or 0 for s in batting_stats)
    fifties = sum(1 for s in batting_stats if 50 <= (s.runs or 0) < 100)
    hundreds = sum(1 for s in batting_stats if (s.runs or 0) >= 100)
    dismissals = sum(1 for s in batting_stats if s.dismissal_type and s.dismissal_type != 'Not out')
    batting_avg = round(total_runs / dismissals, 2) if dismissals > 0 else (float(total_runs) if total_runs > 0 else None)

    # Best bowling calculation
    best_wickets = 0
    best_runs = 999
    best_bowling_str = '—'
    four_wickets = 0
    five_wickets = 0
    dot_balls = sum(s.dot_balls or 0 for s in bowling_stats)

    for s in bowling_stats:
        w = s.wickets or 0
        rc = s.runs_conceded or 0
        if w >= 5:
            five_wickets += 1
        elif w == 4:
            four_wickets += 1
        if w > best_wickets or (w == best_wickets and w > 0 and rc < best_runs):
            best_wickets = w
            best_runs = rc
            best_bowling_str = f"{best_wickets}/{best_runs}"

    # Also compute overs bowled properly
    total_balls_bowled = sum(int(s.overs or 0) * 6 + int(round(((s.overs or 0) - int(s.overs or 0)) * 10)) for s in bowling_stats)
    total_overs_decimal = total_balls_bowled / 6.0 if total_balls_bowled > 0 else 0.0

    career_stats = {
        'matches': len(match_ids),
        'innings_batted': len(batting_stats),
        'innings_bowled': len(bowling_stats),
        'total_runs': total_runs,
        'total_wickets': sum(s.wickets or 0 for s in bowling_stats),
        'highest_score': max((s.runs or 0 for s in batting_stats), default=0),
        'strike_rate': round(total_runs / balls_faced * 100, 2) if balls_faced else None,
        'batting_average': batting_avg,
        'fours': fours,
        'sixes': sixes,
        'fifties': fifties,
        'hundreds': hundreds,
        'economy': round(runs_conceded / total_overs_decimal, 2) if total_overs_decimal else None,
        'best_bowling': best_bowling_str,
        'four_wickets': four_wickets,
        'five_wickets': five_wickets,
        'dot_balls': dot_balls
    }

    return render_template('players/detail.html',
                           player=player,
                           batting_stats=batting_stats,
                           bowling_stats=bowling_stats,
                           career_stats=career_stats)


@app.route('/matches')
def matches():
    """Matches listing page"""
    try:
        season_filter = request.args.get('season', '')
        page = request.args.get('page', 1, type=int)

        query = Match.query.options(joinedload(Match.home_team_obj), joinedload(Match.away_team_obj))
        if season_filter.isdigit():
            query = query.filter(Match.season == int(season_filter))
        else:
            season_filter = ''

        matches_list = (query.order_by(Match.match_date.desc())
                             .paginate(page=page, per_page=15, error_out=False))

        # One scalar query for the filter options instead of hydrating every match.
        seasons = sorted([row[0] for row in db.session.query(distinct(Match.season)).all()], reverse=True)

        return render_template('matches/index.html',
                               matches=matches_list.items,
                               pagination=matches_list,
                               seasons=seasons,
                               selected_season=season_filter)
    except Exception as e:
        app.logger.exception('Error on matches route: %s', e)
        return render_template('matches/index.html',
                               matches=[], pagination=None, seasons=[], selected_season='')


@app.route('/matches/<int:match_id>')
def match_detail(match_id):
    """Match detail page"""
    match = (Match.query
             .options(joinedload(Match.home_team_obj), joinedload(Match.away_team_obj))
             .get_or_404(match_id))

    player_with_team = joinedload(BattingStatistic.player).joinedload(Player.team)
    batting_stats = (BattingStatistic.query
                     .options(player_with_team)
                     .filter_by(match_id=match_id)
                     .order_by(BattingStatistic.runs.desc())
                     .all())
    bowling_stats = (BowlingStatistic.query
                     .options(joinedload(BowlingStatistic.player).joinedload(Player.team))
                     .filter_by(match_id=match_id)
                     .order_by(BowlingStatistic.wickets.desc())
                     .all())

    return render_template('matches/detail.html',
                           match=match,
                           batting_stats=batting_stats,
                           bowling_stats=bowling_stats)


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    try:
        return jsonify(_dashboard_stats())
    except Exception as e:
        app.logger.exception('Error on api_stats: %s', e)
        return jsonify({'error': 'Could not load statistics.'}), 500


@app.route('/analytics')
def analytics():
    """Advanced Analytics Dashboard"""
    return render_template('analytics/index.html')


@app.route('/api/analytics/team_trends')
def api_team_trends():
    """API for team performance trends"""
    try:
        stats = (TeamStatistic.query
                 .options(joinedload(TeamStatistic.team))
                 .order_by(TeamStatistic.season)
                 .all())

        data = {}
        for stat in stats:
            if not stat.team:
                continue
            bucket = data.setdefault(stat.team.short_name, {'seasons': [], 'wins': []})
            bucket['seasons'].append(stat.season)
            bucket['wins'].append(stat.wins)
        return jsonify(data)
    except Exception as e:
        app.logger.exception('Error on api_team_trends: %s', e)
        return jsonify({'error': 'Could not load season trends.'}), 500


@app.route('/predictions')
def predictions():
    """Match Predictions Portal"""
    teams_list = Team.query.order_by(Team.name).all()
    players_list = (Player.query
                    .options(joinedload(Player.team))
                    .filter_by(is_active=True)
                    .order_by(Player.name)
                    .all())
    return render_template('predictions/index.html', teams=teams_list, players=players_list)


@app.route('/api/predict/match')
def api_predict_match():
    """API for match prediction heuristics"""
    team1_id = request.args.get('team1', type=int)
    team2_id = request.args.get('team2', type=int)

    if not team1_id or not team2_id:
        return jsonify({'error': 'Select two teams before running a prediction.'}), 400
    if team1_id == team2_id:
        return jsonify({'error': 'A team cannot play itself — pick two different sides.'}), 400

    try:
        from lib.predictor import MatchPredictor
        result = MatchPredictor().predict(team1_id, team2_id)
        if result.get('error'):
            return jsonify(result), 503
        return jsonify(result)
    except Exception as e:
        app.logger.exception('Error on api_predict_match: %s', e)
        return jsonify({'error': 'The prediction model is unavailable right now.'}), 500


@app.route('/api/predict/player')
def api_predict_player():
    """API for player performance forecasting"""
    player_id = request.args.get('player_id', type=int)
    if not player_id:
        return jsonify({'error': 'Select a player before forecasting.'}), 400

    try:
        from lib.predictor import PlayerForecaster
        result = PlayerForecaster().forecast_runs(player_id)
        if result.get('error'):
            return jsonify(result), 503
        return jsonify(result)
    except Exception as e:
        app.logger.exception('Error on api_predict_player: %s', e)
        return jsonify({'error': 'The forecasting model is unavailable right now.'}), 500


@app.route('/assistant')
def assistant():
    """Smart Team Selection Assistant"""
    teams_list = Team.query.order_by(Team.name).all()
    return render_template('intelligence/assistant.html', teams=teams_list)


@app.route('/api/assistant/team_selection')
def api_team_selection():
    team_id = request.args.get('team_id', type=int)
    opp_id = request.args.get('opponent_id', type=int)

    if not team_id or not opp_id:
        return jsonify({'error': 'Select both your team and an opponent.'}), 400
    if team_id == opp_id:
        return jsonify({'error': 'A team cannot play itself — pick a different opponent.'}), 400

    try:
        from lib.assistant import TeamAssistant
        return jsonify(TeamAssistant().suggest_xi(team_id, opp_id))
    except Exception as e:
        app.logger.exception('Error on api_team_selection: %s', e)
        return jsonify({'error': 'The selection assistant is unavailable right now.'}), 500


@app.route('/player-similarity')
def similarity():
    """Player Similarity Clustering"""
    players_list = (Player.query
                    .options(joinedload(Player.team))
                    .filter_by(is_active=True)
                    .order_by(Player.name)
                    .all())
    return render_template('intelligence/similarity.html', players=players_list)


@app.route('/api/players/similarity')
def api_player_similarity():
    player_id = request.args.get('player_id', type=int)
    if not player_id:
        return jsonify({'error': 'Select a player first.'}), 400

    try:
        from lib.similarity import PlayerSimilarity
        return jsonify(PlayerSimilarity().find_similar(player_id))
    except Exception as e:
        app.logger.exception('Error on api_player_similarity: %s', e)
        return jsonify({'error': 'The clustering model is unavailable right now.'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
