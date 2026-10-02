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

def add_historical_player_season_data():
    """Seed realistic player-season stat records for 2008-2026."""
    with app.app_context():
        from sqlalchemy import text

        if db.session.query(BattingStatistic).count() > 0 or db.session.query(BowlingStatistic).count() > 0:
            print("[v0] Historical batting/bowling stats already exist, skipping...")
            return

        team_map = {
            1: "Mumbai Indians",
            2: "Chennai Super Kings",
            3: "Royal Challengers Bangalore",
            4: "Delhi Capitals",
            5: "Kolkata Knight Riders",
            6: "Rajasthan Royals",
            7: "Punjab Kings",
            8: "Sunrisers Hyderabad",
        }

        players = Player.query.filter_by(is_active=True).all()
        if not players:
            print("[v0] No players found to seed season stats.")
            return

        for season in range(2008, 2027):
            for player in players:
                role = player.role
                matches = random.randint(8, 18)

                if role in ["Batsman", "Wicket-keeper"]:
                    runs = random.randint(250, 2200)
                    balls_faced = random.randint(150, 1800)
                    batting_average = round(runs / max(1, random.randint(6, 18)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(25, 180)
                    fifties = random.randint(0, 12)
                    hundreds = random.randint(0, 3)
                    fours = random.randint(12, 260)
                    sixes = random.randint(2, 70)
                    not_outs = random.randint(0, 6)
                    catches = random.randint(2, 22)
                    stumpings = random.randint(0, 10)
                    run_outs = random.randint(0, 8)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Not Out" if random.random() < 0.2 else "Caught",
                    )
                    db.session.add(batting)

                    overs = round(random.uniform(0.0, 5.0), 1)
                    wickets = random.randint(0, 4)
                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=overs,
                        maidens=0,
                        runs_conceded=random.randint(10, 80),
                        wickets=wickets,
                        economy_rate=round(random.uniform(6.0, 10.0), 2),
                        dot_balls=random.randint(4, 20),
                    )
                    db.session.add(bowling)

                elif role == "Bowler":
                    runs = random.randint(20, 500)
                    balls_faced = random.randint(30, 900)
                    batting_average = round(runs / max(1, random.randint(4, 12)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(8, 90)
                    fifties = random.randint(0, 2)
                    hundreds = 0
                    fours = random.randint(0, 40)
                    sixes = random.randint(0, 18)
                    not_outs = random.randint(0, 4)
                    catches = random.randint(0, 16)
                    stumpings = 0
                    run_outs = random.randint(0, 3)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Bowled",
                    )
                    db.session.add(batting)

                    overs = round(random.uniform(12.0, 90.0), 1)
                    wickets = random.randint(5, 40)
                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=overs,
                        maidens=random.randint(0, 10),
                        runs_conceded=random.randint(120, 1100),
                        wickets=wickets,
                        economy_rate=round(random.uniform(6.0, 9.5), 2),
                        dot_balls=random.randint(25, 220),
                    )
                    db.session.add(bowling)

                else:
                    runs = random.randint(200, 1800)
                    balls_faced = random.randint(120, 1400)
                    batting_average = round(runs / max(1, random.randint(5, 18)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(20, 140)
                    fifties = random.randint(0, 8)
                    hundreds = random.randint(0, 2)
                    fours = random.randint(10, 200)
                    sixes = random.randint(2, 60)
                    not_outs = random.randint(0, 6)
                    catches = random.randint(3, 22)
                    stumpings = random.randint(0, 6)
                    run_outs = random.randint(0, 6)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Caught",
                    )
                    db.session.add(batting)

                    overs = round(random.uniform(8.0, 60.0), 1)
                    wickets = random.randint(4, 25)
                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=overs,
                        maidens=random.randint(0, 8),
                        runs_conceded=random.randint(80, 700),
                        wickets=wickets,
                        economy_rate=round(random.uniform(6.5, 9.0), 2),
                        dot_balls=random.randint(15, 180),
                    )
                    db.session.add(bowling)

        db.session.commit()
        print("[v0] Historical player season stats seeded for 2008-2026.")


        def add_historical_player_season_data():
    """Seed realistic player-season stat records for 2008-2026."""
    with app.app_context():
        if db.session.query(BattingStatistic).count() > 0 or db.session.query(BowlingStatistic).count() > 0:
            print("[v0] Historical batting/bowling stats already exist, skipping...")
            return

        players = Player.query.filter_by(is_active=True).all()
        if not players:
            print("[v0] No players found to seed season stats.")
            return

        for season in range(2008, 2027):
            for player in players:
                role = player.role
                matches = random.randint(8, 18)

                if role in ["Batsman", "Wicket-keeper"]:
                    runs = random.randint(250, 2200)
                    balls_faced = random.randint(150, 1800)
                    batting_average = round(runs / max(1, random.randint(6, 18)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(25, 180)
                    fifties = random.randint(0, 12)
                    hundreds = random.randint(0, 3)
                    fours = random.randint(12, 260)
                    sixes = random.randint(2, 70)
                    not_outs = random.randint(0, 6)
                    catches = random.randint(2, 22)
                    stumpings = random.randint(0, 10)
                    run_outs = random.randint(0, 8)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Not Out" if random.random() < 0.2 else "Caught",
                    )
                    db.session.add(batting)

                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=round(random.uniform(0.0, 5.0), 1),
                        maidens=0,
                        runs_conceded=random.randint(10, 80),
                        wickets=random.randint(0, 4),
                        economy_rate=round(random.uniform(6.0, 10.0), 2),
                        dot_balls=random.randint(4, 20),
                    )
                    db.session.add(bowling)

                elif role == "Bowler":
                    runs = random.randint(20, 500)
                    balls_faced = random.randint(30, 900)
                    batting_average = round(runs / max(1, random.randint(4, 12)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(8, 90)
                    fours = random.randint(0, 40)
                    sixes = random.randint(0, 18)
                    not_outs = random.randint(0, 4)
                    catches = random.randint(0, 16)
                    run_outs = random.randint(0, 3)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Bowled",
                    )
                    db.session.add(batting)

                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=round(random.uniform(12.0, 90.0), 1),
                        maidens=random.randint(0, 10),
                        runs_conceded=random.randint(120, 1100),
                        wickets=random.randint(5, 40),
                        economy_rate=round(random.uniform(6.0, 9.5), 2),
                        dot_balls=random.randint(25, 220),
                    )
                    db.session.add(bowling)

                else:
                    runs = random.randint(200, 1800)
                    balls_faced = random.randint(120, 1400)
                    batting_average = round(runs / max(1, random.randint(5, 18)), 2)
                    strike_rate = round((runs / max(1, balls_faced)) * 100, 2)
                    highest_score = random.randint(20, 140)
                    fifties = random.randint(0, 8)
                    hundreds = random.randint(0, 2)
                    fours = random.randint(10, 200)
                    sixes = random.randint(2, 60)
                    not_outs = random.randint(0, 6)
                    catches = random.randint(3, 22)
                    stumpings = random.randint(0, 6)
                    run_outs = random.randint(0, 6)

                    batting = BattingStatistic(
                        player_id=player.id,
                        match_id=1,
                        runs=runs,
                        balls_faced=balls_faced,
                        fours=fours,
                        sixes=sixes,
                        strike_rate=strike_rate,
                        dismissal_type="Caught",
                    )
                    db.session.add(batting)

                    bowling = BowlingStatistic(
                        player_id=player.id,
                        match_id=1,
                        overs=round(random.uniform(8.0, 60.0), 1),
                        maidens=random.randint(0, 8),
                        runs_conceded=random.randint(80, 700),
                        wickets=random.randint(4, 25),
                        economy_rate=round(random.uniform(6.5, 9.0), 2),
                        dot_balls=random.randint(15, 180),
                    )
                    db.session.add(bowling)

        db.session.commit()
        print("[v0] Historical player season stats seeded for 2008-2026.")

def populate_all():
    """Populate database with all sample data"""
    print("[v0] Starting database initialization...")
    init_database()
    add_sample_teams()
    add_sample_players()
    add_sample_matches()
    add_sample_statistics()
    add_historical_player_season_data()
    print("[v0] Database initialization completed successfully!")

if __name__ == '__main__':
    populate_all()
