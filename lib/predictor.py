import pandas as pd
import numpy as np

from lib.loaders import load_dataset, load_model

class MatchPredictor:
    def __init__(self):
        self.model = load_model('match_predictor.joblib')

    def predict(self, team1_id, team2_id, venue_id=None, toss_winner=None, toss_decision=None):
        if self.model is None:
            return {'error': 'Model not trained yet.'}
            
        # Defaults if not provided
        venue_id = venue_id or team1_id
        toss_winner = toss_winner or team1_id
        toss_decision = toss_decision or 1 # bat
        
        # Prepare input df matching training data
        input_data = pd.DataFrame([{
            'team1': team1_id,
            'team2': team2_id,
            'venue_id': venue_id,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision
        }])
        
        # Predict probabilities
        probs = self.model.predict_proba(input_data)[0]
        classes = list(self.model.classes_)
        
        # Find index for team1 and team2
        prob_team1 = probs[classes.index(team1_id)] if team1_id in classes else 0.5
        prob_team2 = probs[classes.index(team2_id)] if team2_id in classes else 0.5
        
        # Normalize
        total = prob_team1 + prob_team2
        p1 = round((prob_team1 / total) * 100, 1)
        p2 = round((prob_team2 / total) * 100, 1)
        
        # {team1}/{team2} are filled in with the real short names client-side,
        # so the copy reads as a sentence rather than "Team 1".
        if abs(p1 - p2) > 20:
            leader = "{team1}" if p1 > p2 else "{team2}"
            insight = (f"The model strongly favours {leader}, based on historical outcomes "
                       f"at this venue and under this toss decision.")
        elif abs(p1 - p2) > 8:
            leader = "{team1}" if p1 > p2 else "{team2}"
            insight = f"The model leans towards {leader}, but the margin is narrow enough to be overturned."
        else:
            insight = "The model rates this close to even — historical results give neither side a clear edge."


        return {
            'team1': {
                'id': team1_id,
                'win_probability': p1,
                'key_factors': [
                    f'ML assigned base win probability: {p1}%',
                    'Model factors in venue and toss.'
                ]
            },
            'team2': {
                'id': team2_id,
                'win_probability': p2,
                'key_factors': [
                    f'ML assigned base win probability: {p2}%',
                    'Historical constraints evaluated.'
                ]
            },
            'overall_insight': insight
        }

class PlayerForecaster:
    def __init__(self):
        self.model = load_model('player_forecaster.joblib')
        self.df_perf = load_dataset('player_performance_series.csv')

    def forecast_runs(self, player_id):
        if self.model is None or self.df_perf is None:
            return {'error': 'Model not trained.'}
            
        # Get recent 3 matches for player
        p_data = self.df_perf[self.df_perf['player_id'] == player_id].sort_values('match_number', ascending=False).head(3)
        if len(p_data) < 3:
            return {'forecast': 15,
                    'confidence': 'Low — fewer than three recorded innings to learn from'}
            
        runs = p_data['runs_scored'].tolist()
        # [lag_1, lag_2, lag_3] -> recent, previous, older
        input_data = pd.DataFrame([{
            'player_id': player_id,
            'lag_1': runs[0],
            'lag_2': runs[1],
            'lag_3': runs[2]
        }])
        
        pred_runs = self.model.predict(input_data)[0]
        
        return {
            'forecast': round(pred_runs),
            'recent_form': runs,
            'confidence': 'High — modelled on the three most recent innings'
        }
