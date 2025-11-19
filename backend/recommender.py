import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sqlmodel import Session, select
from models import Track
from database import engine

class MusicRecommender:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.df = None
        self.feature_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']

    def load_and_train(self):
        """Loads data from SQL and trains the KNN model in memory."""
        print("Loading data from DB...")
        with Session(engine) as session:
            tracks = session.exec(select(Track)).all()
            self.df = pd.DataFrame([t.dict() for t in tracks])
        
        print("Training KNN Model...")
        # Normalize features
        self.df[self.feature_cols] = self.scaler.fit_transform(self.df[self.feature_cols])
        
        # Init KNN (Euclidean distance)
        self.model = NearestNeighbors(n_neighbors=11, algorithm='auto')
        self.model.fit(self.df[self.feature_cols])
        print("Model Trained!")

    def find_similar(self, input_features: dict):
        # Convert input to dataframe and scale
        input_df = pd.DataFrame([input_features])
        # Ensure columns match
        input_df = input_df[self.feature_cols]
        input_scaled = self.scaler.transform(input_df)
        
        # Find neighbors
        distances, indices = self.model.kneighbors(input_scaled)
        
        # Get results (skip 0 because that's the input itself if it exists in DB, 
        # but since input is external, we take all 10)
        result_indices = indices[0][1:] 
        results = self.df.iloc[result_indices]
        
        # Return original data (inverse transform if we wanted exact values, 
        # but we just want IDs and Names)
        return results[['name', 'artist', 'id']].to_dict(orient='records')
