from models import Player, db

from lib.loaders import load_dataset

class TeamAssistant:
    def __init__(self):
        self.df_clusters = load_dataset('player_clusters.csv')

    def suggest_xi(self, team_id, opponent_id):
        if self.df_clusters is None:
            return {'error': 'Clustering data not found.'}
            
        # Get all players for this team from DB
        squad = Player.query.filter_by(team_id=team_id, is_active=True).all()
        if not squad:
            return {'error': 'No players found for this team.'}
            
        # A simple heuristic: Try to pick top 5 batsmen, 1 wicket-keeper, 2 all-rounders, 3 bowlers
        # If we don't have exact numbers, just pick best available
        roles_needed = {
            'Batsman': 5,
            'Wicket-keeper': 1,
            'All-rounder': 2,
            'Bowler': 3
        }
        
        selected = []
        for role, count in roles_needed.items():
            candidates = [p for p in squad if p.role == role]
            # Randomly select for now (in real life, rank by recent form or match with opponent weaknesses)
            # We'll just take the first N
            selected.extend(candidates[:count])
            
        # Fallback if we didn't get 11
        if len(selected) < 11:
            remaining = [p for p in squad if p not in selected]
            needed = 11 - len(selected)
            selected.extend(remaining[:needed])
            
        # Describe the XI that was actually picked. The previous copy claimed a
        # fixed 5/1/2/3 split and an opponent-weakness analysis that this
        # heuristic does not perform.
        labels = {
            'Batsman': ('batter', 'batters'),
            'Wicket-keeper': ('keeper', 'keepers'),
            'All-rounder': ('all-rounder', 'all-rounders'),
            'Bowler': ('bowler', 'bowlers'),
        }

        counts = {}
        for player in selected:
            counts[player.role] = counts.get(player.role, 0) + 1

        breakdown = ', '.join(
            f'{counts[role]} {labels[role][0] if counts[role] == 1 else labels[role][1]}'
            for role in labels
            if counts.get(role)
        )

        return {
            'team_id': team_id,
            'opponent_id': opponent_id,
            'suggested_xi': [{'id': p.id, 'name': p.name, 'role': p.role} for p in selected],
            'reasoning': (
                f'Picked {breakdown} — the closest fit the available squad allows '
                f'to a 5/1/2/3 balance.'
            )
        }
