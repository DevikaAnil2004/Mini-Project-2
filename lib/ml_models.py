import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self):
        os.makedirs('models', exist_ok=True)
        
    def train_match_predictor(self):
        print("Training Match Outcome Predictor...")
        try:
            df = pd.read_csv('data/historical_matches.csv')
            
            # Features: team1, team2, venue_id, toss_winner, toss_decision
            X = df[['team1', 'team2', 'venue_id', 'toss_winner', 'toss_decision']]
            y = df['winner']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            accuracy = model.score(X_test, y_test)
            print(f"Match Predictor Accuracy: {accuracy:.2f}")
            
            joblib.dump(model, 'models/match_predictor.joblib')
            return True
        except Exception as e:
            print(f"Error training match predictor: {e}")
            return False

    def train_player_forecaster(self):
        print("Training Player Performance Forecaster...")
        try:
            df = pd.read_csv('data/player_performance_series.csv')
            
            # Simple autoregressive feature: previous 3 matches
            # Since data is sequential, we shift to create lag features
            df['lag_1'] = df.groupby('player_id')['runs_scored'].shift(1)
            df['lag_2'] = df.groupby('player_id')['runs_scored'].shift(2)
            df['lag_3'] = df.groupby('player_id')['runs_scored'].shift(3)
            
            df = df.dropna()
            
            X = df[['player_id', 'lag_1', 'lag_2', 'lag_3']]
            y = df['runs_scored']
            
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X, y)
            
            joblib.dump(model, 'models/player_forecaster.joblib')
            print("Player Forecaster trained successfully.")
            return True
        except Exception as e:
            print(f"Error training player forecaster: {e}")
            return False

    def train_player_clustering(self):
        print("Training Player Clustering (Similarity)...")
        try:
            df = pd.read_csv('data/player_stats.csv')
            
            # We cluster based on role-agnostic numerical stats to find playing styles
            features = ['batting_average', 'strike_rate', 'wickets', 'economy_rate']
            X = df[features]
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=8, random_state=42, n_init=10)
            df['cluster'] = kmeans.fit_predict(X_scaled)
            
            joblib.dump(kmeans, 'models/player_clustering.joblib')
            joblib.dump(scaler, 'models/player_scaler.joblib')
            df.to_csv('data/player_clusters.csv', index=False)
            
            print("Player Clustering trained successfully.")
            return True
        except Exception as e:
            print(f"Error training player clustering: {e}")
            return False

def train_all():
    trainer = ModelTrainer()
    trainer.train_match_predictor()
    trainer.train_player_forecaster()
    trainer.train_player_clustering()

if __name__ == '__main__':
    train_all()
