import os
from flask import Flask, render_template, request, jsonify
from config import config
from models import db, Team, Player, Match, BattingStatistic, BowlingStatistic, TeamStatistic
from datetime import datetime

app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)


@app.before_request
def before_request():
    """Execute before each request"""
    pass


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    try:
        total_teams = Team.query.count()
        total_players = Player.query.count()
        total_matches = Match.query.count()
        
        # Get latest matches
        latest_matches = Match.query.order_by(Match.match_date.desc()).limit(5).all()
        
        stats = {
            'total_teams': total_teams,
            'total_players': total_players,
            'total_matches': total_matches
        }
        
        return render_template('index.html', stats=stats, latest_matches=latest_matches)
    except Exception as e:
        print(f"[v0] Error on index route: {str(e)}")
        return render_template('index.html', stats={}, latest_matches=[])


@app.route('/teams')
def teams():
    """Teams listing page"""
    try:
        page = request.args.get('page', 1, type=int)
        teams_list = Team.query.paginate(page=page, per_page=12)
        return render_template('teams/index.html', teams=teams_list.items, pagination=teams_list)
    except Exception as e:
        print(f"[v0] Error on teams route: {str(e)}")
        return render_template('teams/index.html', teams=[], pagination=None)


@app.route('/teams/<int:team_id>')
def team_detail(team_id):
    """Team detail page"""
    try:
        team = Team.query.get_or_404(team_id)
        players = Player.query.filter_by(team_id=team_id, is_active=True).all()
        stats = TeamStatistic.query.filter_by(team_id=team_id).order_by(TeamStatistic.season.desc()).first()
        return render_template('teams/detail.html', team=team, players=players, stats=stats)
    except Exception as e:
        print(f"[v0] Error on team_detail route: {str(e)}")
        return render_template('404.html'), 404


@app.route('/players')
def players():
    """Players listing page"""
    try:
        role_filter = request.args.get('role', '')
        page = request.args.get('page', 1, type=int)
        
        query = Player.query.filter_by(is_active=True)
        if role_filter:
            query = query.filter_by(role=role_filter)
        
        players_list = query.paginate(page=page, per_page=20)
        roles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper']
        
        return render_template('players/index.html', 
                             players=players_list.items, 
                             pagination=players_list,
                             roles=roles,
                             selected_role=role_filter)
    except Exception as e:
        print(f"[v0] Error on players route: {str(e)}")
        return render_template('players/index.html', 
                             players=[], 
                             pagination=None,
                             roles=[],
                             selected_role='')


@app.route('/players/<int:player_id>')
def player_detail(player_id):
    """Player detail page"""
    try:
        player = Player.query.get_or_404(player_id)
        batting_stats = BattingStatistic.query.filter_by(player_id=player_id).all()
        bowling_stats = BowlingStatistic.query.filter_by(player_id=player_id).all()
        
        # Calculate career stats
        career_stats = {
            'matches': len(batting_stats) + len(bowling_stats),
            'total_runs': sum(b.runs for b in batting_stats),
            'total_wickets': sum(b.wickets for b in bowling_stats),
        }
        
        return render_template('players/detail.html', 
                             player=player, 
                             batting_stats=batting_stats,
                             bowling_stats=bowling_stats,
                             career_stats=career_stats)
    except Exception as e:
        print(f"[v0] Error on player_detail route: {str(e)}")
        return render_template('404.html'), 404


@app.route('/matches')
def matches():
    """Matches listing page"""
    try:
        season_filter = request.args.get('season', '')
        page = request.args.get('page', 1, type=int)
        
        query = Match.query
        if season_filter:
            query = query.filter_by(season=int(season_filter))
        
        matches_list = query.order_by(Match.match_date.desc()).paginate(page=page, per_page=15)
        seasons = [m.season for m in Match.query.distinct(Match.season).all()]
        
        return render_template('matches/index.html', 
                             matches=matches_list.items,
                             pagination=matches_list,
                             seasons=seasons,
                             selected_season=season_filter)
    except Exception as e:
        print(f"[v0] Error on matches route: {str(e)}")
        return render_template('matches/index.html', 
                             matches=[],
                             pagination=None,
                             seasons=[],
                             selected_season='')


@app.route('/matches/<int:match_id>')
def match_detail(match_id):
    """Match detail page"""
    try:
        match = Match.query.get_or_404(match_id)
        batting_stats = BattingStatistic.query.filter_by(match_id=match_id).all()
        bowling_stats = BowlingStatistic.query.filter_by(match_id=match_id).all()
        
        return render_template('matches/detail.html',
                             match=match,
                             batting_stats=batting_stats,
                             bowling_stats=bowling_stats)
    except Exception as e:
        print(f"[v0] Error on match_detail route: {str(e)}")
        return render_template('404.html'), 404


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = {
            'total_teams': Team.query.count(),
            'total_players': Player.query.count(),
            'total_matches': Match.query.count(),
            'completed_matches': Match.query.filter_by(status='completed').count()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        print("[v0] Creating database tables...")
        db.create_all()
        print("[v0] Database tables created successfully!")
    
    print("[v0] Starting Flask development server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
