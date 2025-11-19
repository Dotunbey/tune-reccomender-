import httpx
import base64
import os

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token = None

    async def authenticate(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_b64 = base64.b64encode(auth_string.encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.spotify.com/api/token",
                data={"grant_type": "client_credentials"},
                headers={"Authorization": f"Basic {auth_b64}"}
            )
            self.token = response.json().get("access_token")

    async def search_track(self, query: str):
        if not self.token: await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spotify.com/v1/search",
                params={"q": query, "type": "track", "limit": 1},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            tracks = response.json().get("tracks", {}).get("items", [])
            return tracks[0] if tracks else None

    async def get_audio_features(self, track_id: str):
        if not self.token: await self.authenticate()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.spotify.com/v1/audio-features/{track_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()
