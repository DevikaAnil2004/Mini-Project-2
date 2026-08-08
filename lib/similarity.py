from models import Player

from lib.loaders import load_dataset

class PlayerSimilarity:
    def __init__(self):
        self.df_clusters = load_dataset('player_clusters.csv')

    def find_similar(self, player_id):
        if self.df_clusters is None:
            return {'error': 'Clustering data not found.'}
            
        player_row = self.df_clusters[self.df_clusters['player_id'] == player_id]
        if player_row.empty:
            return {'error': 'Player not found in statistical data.'}
            
        cluster_id = player_row.iloc[0]['cluster']
        role = player_row.iloc[0]['role']
        
        # Find others in same cluster and role
        similar_df = self.df_clusters[(self.df_clusters['cluster'] == cluster_id) & 
                                      (self.df_clusters['player_id'] != player_id) &
                                      (self.df_clusters['role'] == role)].head(5)
                                      
        similar_players = []
        for _, row in similar_df.iterrows():
            p_obj = Player.query.get(row['player_id'])
            if p_obj:
                similar_players.append({
                    'id': p_obj.id,
                    'name': p_obj.name,
                    'role': p_obj.role,
                    'team': p_obj.team.short_name if p_obj.team else None
                })
                
        return {
            'target_player_id': player_id,
            'cluster_id': int(cluster_id),
            'similar_players': similar_players
        }
