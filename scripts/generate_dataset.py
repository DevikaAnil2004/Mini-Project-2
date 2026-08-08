import pandas as pd
import numpy as np
import os
import random
import sqlite3

def generate_datasets():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # 1. Generate Match Data (for Outcome Predictor)
    print("Generating synthetic match data...")
    num_matches = 2000
    teams = [1, 2, 3, 4, 5, 6, 7, 8]
    venues = ['Wankhede Stadium', 'M. A. Chidambaram Stadium', 'M. Chinnaswamy Stadium', 
              'Arun Jaitley Stadium', 'Eden Gardens', 'Sawai Mansingh Stadium', 
              'PCA Stadium', 'Rajiv Gandhi Intl Cricket Stadium']
    
    match_data = []
    for _ in range(num_matches):
        t1, t2 = random.sample(teams, 2)
        venue_id = random.choice([t1, t2, random.choice(teams)])
        venue = venues[venue_id - 1]
        
        # Features
        toss_winner = random.choice([t1, t2])
        toss_decision = random.choice(['bat', 'field'])
        
        # Add some bias based on toss and home advantage
        t1_prob = 0.5
        if toss_winner == t1: t1_prob += 0.05
        if venue_id == t1: t1_prob += 0.05
        if venue_id == t2: t1_prob -= 0.05
        
        winner = t1 if random.random() < t1_prob else t2
        
        match_data.append({
            'team1': t1,
            'team2': t2,
            'venue_id': venue_id,
            'toss_winner': toss_winner,
            'toss_decision': 1 if toss_decision == 'bat' else 0,
            'winner': winner
        })
        
    df_matches = pd.DataFrame(match_data)
    df_matches.to_csv('data/historical_matches.csv', index=False)
    
    # 2. Generate Player Stats Data (for Similarity and Forecasting)
    print("Fetching real players from database...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'cricketiq.db')
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run init_db.py first.")
        return
        
    conn = sqlite3.connect(db_path)
    # Fetch all players
    players_df = pd.read_sql_query("SELECT id, name, role FROM players", conn)
    conn.close()
    
    if len(players_df) == 0:
        print("Error: No players found in database. Run init_db.py first.")
        return
        
    print(f"Generating synthetic stats for {len(players_df)} real players...")
    
    player_data = []
    for index, row in players_df.iterrows():
        pid = row['id']
        role = row['role']
        
        # Base stats
        matches = random.randint(10, 150)
        
        if role in ['Batsman', 'Wicket-keeper']:
            runs = int(matches * random.uniform(20, 45))
            strike_rate = random.uniform(120.0, 160.0)
            average = random.uniform(25.0, 45.0)
            wickets = random.randint(0, 5)
            economy = random.uniform(7.5, 12.0)
        elif role == 'Bowler':
            runs = int(matches * random.uniform(2, 10))
            strike_rate = random.uniform(80.0, 120.0)
            average = random.uniform(5.0, 15.0)
            wickets = int(matches * random.uniform(0.8, 1.8))
            economy = random.uniform(6.0, 8.5)
        else: # All-rounder
            runs = int(matches * random.uniform(15, 30))
            strike_rate = random.uniform(115.0, 145.0)
            average = random.uniform(18.0, 32.0)
            wickets = int(matches * random.uniform(0.5, 1.2))
            economy = random.uniform(7.0, 9.0)
            
        player_data.append({
            'player_id': pid,
            'role': role,
            'matches': matches,
            'runs': runs,
            'batting_average': average,
            'strike_rate': strike_rate,
            'wickets': wickets,
            'economy_rate': economy
        })
        
    df_players = pd.DataFrame(player_data)
    df_players.to_csv('data/player_stats.csv', index=False)
    
    # 3. Generate Player Match-by-Match (for Forecasting)
    print("Generating player match-by-match series...")
    performance_series = []
    for pid in df_players['player_id']:
        p_row = df_players[df_players['player_id'] == pid].iloc[0]
        role = p_row['role']
        num_m = p_row['matches']
        
        # Random walk for runs
        base_runs = 30 if role in ['Batsman', 'Wicket-keeper'] else (15 if role == 'All-rounder' else 5)
        current_form = base_runs
        
        for m in range(1, num_m + 1):
            runs = max(0, int(np.random.normal(current_form, 15)))
            current_form = current_form * 0.8 + runs * 0.2 # form updates
            
            performance_series.append({
                'player_id': pid,
                'match_number': m,
                'runs_scored': runs
            })
            
    df_perf = pd.DataFrame(performance_series)
    df_perf.to_csv('data/player_performance_series.csv', index=False)
    
    print("Datasets generated successfully in 'data/' directory.")

if __name__ == '__main__':
    generate_datasets()
