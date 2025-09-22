# main.py
# VibeCheck - get Spotify song recommendations by mood or genre

from spotify_api import get_access_token, get_recommendations
from mood_map import get_audio_features_for_mood

# Spotify-supported safe genres for example fallback
VALID_GENRES = ["pop", "rock", "hip-hop", "dance", "r-n-b", "indie"]

print("🎵 Welcome to VibeCheck! 🎵")
print("You can pick a mood or a genre to get some song recommendations.\n")

# Ask for mood
mood = input("Enter your mood: ").lower()
features = get_audio_features_for_mood(mood)

# Get Spotify access token
token = get_access_token()

# Determine genre from mood or ask for genre
if features:
    genre = features.get("genre", "pop")  # default to pop if genre missing
    print(f"\nFetching Spotify tracks for '{mood}' mood ({genre} genre)...")
    tracks = get_recommendations(token=token, genre=genre, limit=5)
else:
    print(f"⚠️ Mood '{mood}' not recognized. Let's try a genre instead.")
    print("Example genres: pop, rock, hip-hop")
    genre_input = input("Enter a genre: ").lower()
    limit_input = input("How many tracks would you like to see? (default 5): ")
    limit = int(limit_input) if limit_input.isdigit() else 5

    if genre_input in VALID_GENRES:
        tracks = get_recommendations(token=token, genre=genre_input, limit=limit)
    else:
        print(f"⚠️ Genre '{genre_input}' not supported. Attempting artist radio fallback...")
        tracks = get_recommendations(token=token, limit=limit, artist_seed=genre_input)

# Print tracks
if tracks:
    print("\n🎧 Here are your recommendations:")
    for t in tracks:
        name = t["name"]
        artist_list = ", ".join(t["artists"])
        url = t["external_urls"]["spotify"]
        print(f"- {name} by {artist_list} → {url}")
else:
    print("⚠️ No tracks found. Try a different mood or genre!")
