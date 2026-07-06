from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Team(db.Model):
    """IPL Team Model"""
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    short_name = db.Column(db.String(10), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    home_ground = db.Column(db.String(100))
    founded_year = db.Column(db.Integer)
    owner = db.Column(db.String(150))
    coach = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    players = db.relationship('Player', backref='team', lazy=True, cascade='all, delete-orphan')
    matches_home = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team_obj')
    matches_away = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team_obj')
    
    def __repr__(self):
        return f'<Team {self.name}>'


class Player(db.Model):
    """Cricket Player Model"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    jersey_number = db.Column(db.Integer)
    role = db.Column(db.String(50), nullable=False)  # Batsman, Bowler, All-rounder, Wicket-keeper
    batting_style = db.Column(db.String(50))  # Right-handed, Left-handed
    bowling_style = db.Column(db.String(50))  # Right-arm fast, Left-arm spinner, etc.
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batting_stats = db.relationship('BattingStatistic', backref='player', lazy=True)
    bowling_stats = db.relationship('BowlingStatistic', backref='player', lazy=True)
    
    def __repr__(self):
        return f'<Player {self.name}>'


class Match(db.Model):
    """Match Model"""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, nullable=False)  # IPL season number
    match_number = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(150))
    status = db.Column(db.String(50), default='scheduled')  # scheduled, live, completed, cancelled
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    man_of_the_match = db.Column(db.String(150))
    toss_winner_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    toss_decision = db.Column(db.String(50))  # bat or bowl
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Match {self.season}-{self.match_number}>'


class BattingStatistic(db.Model):
    """Batting Statistics Model"""
    __tablename__ = 'batting_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    runs = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    strike_rate = db.Column(db.Float)
    dismissal_type = db.Column(db.String(50))  # Bowled, Caught, LBW, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    match = db.relationship('Match', backref='batting_stats')
    
    def __repr__(self):
        return f'<BattingStats {self.player_id}-{self.match_id}>'


class BowlingStatistic(db.Model):
    """Bowling Statistics Model"""
    __tablename__ = 'bowling_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    overs = db.Column(db.Float)
    maidens = db.Column(db.Integer, default=0)
    runs_conceded = db.Column(db.Integer, default=0)
    wickets = db.Column(db.Integer, default=0)
    economy_rate = db.Column(db.Float)
    dot_balls = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    match = db.relationship('Match', backref='bowling_stats')
    
    def __repr__(self):
        return f'<BowlingStats {self.player_id}-{self.match_id}>'


class TeamStatistic(db.Model):
    """Team Season Statistics Model"""
    __tablename__ = 'team_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    position = db.Column(db.Integer)
    points = db.Column(db.Integer, default=0)
    run_rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = db.relationship('Team', backref='statistics')
    
    def __repr__(self):
        return f'<TeamStatistic {self.team_id}-{self.season}>'
