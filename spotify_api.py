# spotify_api.py
# VibeCheck - Spotify integration for fetching song recommendations

import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# Fetch your Spotify credentials from .env
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify-supported seed genres (official)
VALID_GENRES = [
    "acoustic", "afrobeat", "alt-rock", "ambient", "country", "dance",
    "deep-house", "disco", "edm", "electronic", "folk", "funk", "hip-hop",
    "indie", "jazz", "k-pop", "latin", "metal", "pop", "punk", "r-n-b",
    "reggae", "rock", "soul", "techno", "trance", "trap", "vocal"
]


def get_access_token():
    """
    Request an access token from Spotify using client credentials.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise Exception("⚠️ Missing Spotify Client ID or Secret. Check your .env file!")

    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"⚠️ Couldn't get access token: {response.status_code}")

    return response.json()["access_token"]


def get_recommendations(token, limit=5, genre=None, artist_seed=None):
    """
    Fetch Spotify track recommendations.
    - Provide either a genre or an artist seed.
    """
    endpoint = "https://api.spotify.com/v1/recommendations"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit}

    # Decide whether to use genre or artist seed
    if genre and genre.lower() in VALID_GENRES:
        params["seed_genres"] = genre.lower()
    elif artist_seed:
        # Use artist name search to get artist ID
        artist_id = _get_artist_id(artist_seed, token)
        if artist_id:
            params["seed_artists"] = artist_id
        else:
            print(f"⚠️ Artist '{artist_seed}' not found. Using default genre 'pop'.")
            params["seed_genres"] = "pop"
    else:
        params["seed_genres"] = "pop"  # default fallback

    # Request recommendations
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"⚠️ Failed to get recommendations: {response.status_code}")

    tracks = response.json().get("tracks", [])
    return [
        {
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "external_urls": track["external_urls"]
        }
        for track in tracks
    ]


def _get_artist_id(artist_name, token):
    """
    Search Spotify for an artist and return their ID.
    """
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code != 200:
        return None

    artists = response.json().get("artists", {}).get("items", [])
    if artists:
        return artists[0]["id"]
    return None
