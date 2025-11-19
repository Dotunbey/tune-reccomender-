import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Model ---
class Track(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    artist: str
    danceability: float
    energy: float
    valence: float
    tempo: float
    acousticness: float
    instrumentalness: float

# --- Config ---
DATABASE_URL = os.getenv("DATABASE_URL")
CSV_PATH = "data/tracks.csv" # You must download the Spotify Dataset from Kaggle
SAMPLE_SIZE = 50000 

def load_data():
    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)
    
    # Filter and Clean
    needed_cols = ['id', 'name', 'artists', 'danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']
    df = df[needed_cols].dropna()
    
    # Clean artist name (remove [' '])
    df['artists'] = df['artists'].str.replace(r"['\[\]]", "", regex=True)
    
    # Sample
    df = df.sample(n=SAMPLE_SIZE, random_state=42)
    
    print(f"Loading {len(df)} tracks into database...")
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Bulk insert
        tracks = []
        for _, row in df.iterrows():
            tracks.append(Track(
                id=row['id'],
                name=row['name'],
                artist=row['artists'],
                danceability=row['danceability'],
                energy=row['energy'],
                valence=row['valence'],
                tempo=row['tempo'],
                acousticness=row['acousticness'],
                instrumentalness=row['instrumentalness']
            ))
        
        session.add_all(tracks)
        session.commit()
    print("Success! Database populated.")

if __name__ == "__main__":
    load_data()
