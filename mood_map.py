# mood_map.py
# VibeCheck - get audio features for a mood

import json
import os

MOODS_FILE = os.path.join(os.path.dirname(__file__), "moods.json")

def get_audio_features_for_mood(mood: str):
    """
    Returns a dict of audio features for a given mood.
    If mood is not found, returns None.
    """
    mood = mood.lower()
    try:
        with open(MOODS_FILE, "r") as f:
            moods = json.load(f)
    except FileNotFoundError:
        print("⚠️ moods.json file not found!")
        return None

    return moods.get(mood)
