from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from recommender import MusicRecommender
from spotify_client import SpotifyClient

# Initialize Recommender and Spotify Client
recommender = MusicRecommender()
spotify = SpotifyClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Train model on startup
    recommender.load_and_train()
    yield

app = FastAPI(lifespan=lifespan)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "TuneTexture API is Live"}

@app.get("/recommend")
async def recommend(song: str):
    # 1. Find song on Spotify
    track = await spotify.search_track(song)
    if not track:
        raise HTTPException(status_code=404, detail="Song not found on Spotify")
    
    # 2. Get Audio Features
    features = await spotify.get_audio_features(track['id'])
    
    # 3. Get Recommendations from AI
    # Prepare features dictionary matches our model columns
    input_feats = {
        'danceability': features['danceability'],
        'energy': features['energy'],
        'valence': features['valence'],
        'tempo': features['tempo'],
        'acousticness': features['acousticness'],
        'instrumentalness': features['instrumentalness']
    }
    
    recommendations = recommender.find_similar(input_feats)
    
    return {
        "searched_song": {
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "features": input_feats
        },
        "recommendations": recommendations
    }
