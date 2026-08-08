"""
Database initialization script with sample data
Run this script to populate the database with sample IPL data
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from models import db, Team, Player, Match, BattingStatistic, BowlingStatistic, TeamStatistic

# Initialize Flask app
app = Flask(__name__)
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])
db.init_app(app)


def init_database():
    """Initialize database with tables"""
    with app.app_context():
        print("[v0] Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        print("[v0] Database tables created successfully!")
        print("[v0] Database tables created successfully!")


def add_sample_teams():
    """Add sample IPL teams"""
    with app.app_context():
        # Check if teams already exist
        if Team.query.count() > 0:
            print("[v0] Teams already exist, skipping...")
            return
        
        teams_data = [
            {
                'name': 'Mumbai Indians',
                'short_name': 'MI',
                'city': 'Mumbai',
                'home_ground': 'Wankhede Stadium',
                'founded_year': 2008,
                'owner': 'Reliance Industries',
                'coach': 'Mahela Jayawardene'
            },
            {
                'name': 'Chennai Super Kings',
                'short_name': 'CSK',
                'city': 'Chennai',
                'home_ground': 'M. A. Chidambaram Stadium',
                'founded_year': 2008,
                'owner': 'India Cements',
                'coach': 'Stephen Fleming'
            },
            {
                'name': 'Royal Challengers Bangalore',
                'short_name': 'RCB',
                'city': 'Bangalore',
                'home_ground': 'M. Chinnaswamy Stadium',
                'founded_year': 2008,
                'owner': 'United Spirits',
                'coach': 'Andy Flower'
            },
            {
                'name': 'Delhi Capitals',
                'short_name': 'DC',
                'city': 'Delhi',
                'home_ground': 'Arun Jaitley Stadium',
                'founded_year': 2008,
                'owner': 'GMR Group',
                'coach': 'Ricky Ponting'
            },
            {
                'name': 'Kolkata Knight Riders',
                'short_name': 'KKR',
                'city': 'Kolkata',
                'home_ground': 'Eden Gardens',
                'founded_year': 2008,
                'owner': 'Red Chillies Entertainment',
                'coach': 'Brendon McCullum'
            },
            {
                'name': 'Rajasthan Royals',
                'short_name': 'RR',
                'city': 'Jaipur',
                'home_ground': 'Sawai Mansingh Stadium',
                'founded_year': 2008,
                'owner': 'Manoj Badale',
                'coach': 'Kumar Sangakkara'
            },
            {
                'name': 'Punjab Kings',
                'short_name': 'PBKS',
                'city': 'Mohali',
                'home_ground': 'PCA Stadium',
                'founded_year': 2008,
                'owner': 'Ness Wadia Group',
                'coach': 'Ravi Shastri'
            },
            {
                'name': 'Sunrisers Hyderabad',
                'short_name': 'SRH',
                'city': 'Hyderabad',
                'home_ground': 'Rajiv Gandhi Intl Cricket Stadium',
                'founded_year': 2013,
                'owner': 'Sun TV Network',
                'coach': 'Brian Lara'
            },
        ]
        
        for team_data in teams_data:
            team = Team(**team_data)
            db.session.add(team)
        
        db.session.commit()
        print(f"[v0] Added {len(teams_data)} teams")


def add_sample_players():
    """Add real IPL players"""
    with app.app_context():
        # Import real players data
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
        try:
            from real_players_data import real_players_data
        except ImportError as e:
            print(f"[v0] Failed to import real players data: {e}")
            return
            
        players_added = 0
        for team_id, players in real_players_data.items():
            for player_data in players:
                player_data['team_id'] = team_id
                player = Player(**player_data)
                db.session.add(player)
                players_added += 1
        
        db.session.commit()
        print(f"[v0] Added {players_added} players")


def add_sample_matches():
    """Add sample matches"""
    with app.app_context():
        # Check if matches already exist
        if Match.query.count() > 0:
            print("[v0] Matches already exist, skipping...")
            return
        
        base_date = datetime.now() - timedelta(days=30)
        
        matches_data = [
            {
                'season': 16,
                'match_number': 1,
                'home_team_id': 1,
                'away_team_id': 2,
                'match_date': base_date + timedelta(days=1),
                'venue': 'Wankhede Stadium',
                'status': 'completed',
                'home_team_score': 185,
                'away_team_score': 168,
                'winner_id': 1,
                'man_of_the_match': 'Rohit Sharma'
            },
            {
                'season': 16,
                'match_number': 2,
                'home_team_id': 3,
                'away_team_id': 4,
                'match_date': base_date + timedelta(days=2),
                'venue': 'M. Chinnaswamy Stadium',
                'status': 'completed',
                'home_team_score': 175,
                'away_team_score': 162,
                'winner_id': 3,
                'man_of_the_match': 'Virat Kohli'
            },
            {
                'season': 16,
                'match_number': 3,
                'home_team_id': 5,
                'away_team_id': 6,
                'match_date': base_date + timedelta(days=3),
                'venue': 'Eden Gardens',
                'status': 'scheduled',
            },
        ]
        
        for match_data in matches_data:
            match = Match(**match_data)
            db.session.add(match)
        
        db.session.commit()
        print(f"[v0] Added {len(matches_data)} matches")


def add_sample_statistics():
    """Add sample team statistics"""
    with app.app_context():
        # Check if team stats already exist
        if TeamStatistic.query.count() > 0:
            print("[v0] Team statistics already exist, skipping...")
            return
        
        for team_id in range(1, 9):
            stat = TeamStatistic(
                team_id=team_id,
                season=16,
                matches_played=5,
                wins=3,
                losses=2,
                position=team_id,
                points=6,
                run_rate=8.5
            )
            db.session.add(stat)
        
        db.session.commit()
        print("[v0] Added team statistics")


def populate_all():
    """Populate database with all sample data"""
    print("[v0] Starting database initialization...")
    init_database()
    add_sample_teams()
    add_sample_players()
    add_sample_matches()
    add_sample_statistics()
    print("[v0] Database initialization completed successfully!")


if __name__ == '__main__':
    populate_all()
