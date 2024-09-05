import random

from flask import Flask, request, session

from auth import get_client
from color_palettes import color_palettes
from search import SpotifySearch

sp = get_client(session)
search = SpotifySearch(sp)


def process_search_results(results):
    suggestions = []
    for item in results.get("tracks", {}).get("items", []):
        label = f"{', '.join([artist['name'] for artist in item['artists']])} - {item['name']}"
        value = item["id"]
        suggestions.append({"label": label, "value": value, "type": "track"})
    return suggestions


def random_track():
    chars = list("abcdefghijklmnopqrstuvwxyz")
    markets = [
        "AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR",
        "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR",
        "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY",
        "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL",
        "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB",
        "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA",
        "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO",
        "PS", "IN", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS",
        "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG",
        "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ",
        "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW",
        "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS",
        "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL",
        "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM",
        "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW",
        "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM",
        "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"
    ]

    wildcard = ["%", ""]

    random_char = random.choice(chars) # Randomly select letter from list
    random_market = random.choice(markets) # Randomly select a market
    extra_random = random.choice(wildcard) # Randomly select wildcard prefix
    query = extra_random + random_char + "%" # Create query by combining above elements

    print(query, random_market)

    # Pass randomised query to random search method, return set of 33 tracks based on query
    random_result = search.random_search(
        query, search_type="track", market=random_market
    )
    track_id = [track["id"] for track in random_result["tracks"]["items"]] # List of 25 track IDs
    random_track = random.choice(track_id) # Randomly select a track ID from list
    return random_track # Return randomly selected track ID


def get_key_signature(features):
    pitch_classes = {
        0: "C",
        1: "C♯/D♭",
        2: "D",
        3: "D♯/E♭",
        4: "E",
        5: "F",
        6: "F♯/G♭",
        7: "G",
        8: "G♯/A♭",
        9: "A",
        10: "A♯/B♭",
        11: "B",
    }
    key = features.get("key", -1)
    mode = features.get("mode", 0)
    if key == -1:
        return "No key detected"
    pitch = pitch_classes.get(key, "Unknown")
    scale = "major" if mode == 1 else "minor"
    return f"{pitch} {scale}"


def get_loudness(features):
    loudness = features.get("loudness")
    return f"{loudness:.1f} dB"


def get_time_sig(features):
    time_sig = features.get("time_signature")
    return f"{time_sig}/4"


def get_bpm(features):
    bpm = features.get("tempo")
    return bpm


def get_artist_image(track_id):
    artist_id = search.get_artist_id(track_id)
    artist_data = search.get_artist_data(artist_id)
    try:
        image = artist_data["images"][0]["url"]
        return image
    except IndexError:
        return "/static/no_img.png"


def get_artist_genre(track_id):
    artist_id = search.get_artist_id(track_id)
    artist_data = search.get_artist_data(artist_id)
    genres = artist_data["genres"][:5]
    return genres


def get_new_track(track_id):
    new_track_data = search.get_track_recommendation(track_id)
    new_track = new_track_data["tracks"][0]["id"]
    return new_track


def get_related_artists(track_id):
    related_artists_data = search.get_related_artists(track_id)
    related_artists = [artist["name"] for artist in related_artists_data["artists"]][:5]
    return related_artists


def get_valence(features):
    valence = features.get("valence")
    print(f"Valence: {valence}")
    if valence <= 0.125:
        return "V1"
    elif 0.125 < valence <= 0.250:
        return "V2"
    elif 0.250 < valence <= 0.375:
        return "V3"
    elif 0.375 < valence <= 0.500:
        return "V4"
    elif 0.500 < valence <= 0.625:
        return "V5"
    elif 0.625 < valence <= 0.750:
        return "V6"
    elif 0.750 < valence <= 0.875:
        return "V7"
    elif valence > 0.875:
        return "V8"


def get_energy(features):
    energy = features.get("energy")
    print(f"Energy: {energy}")
    if energy <= 0.125:
        return "E1"
    elif 0.125 < energy <= 0.250:
        return "E2"
    elif 0.250 < energy <= 0.375:
        return "E3"
    elif 0.375 < energy <= 0.500:
        return "E4"
    elif 0.500 < energy <= 0.625:
        return "E5"
    elif 0.625 < energy <= 0.750:
        return "E6"
    elif 0.750 < energy <= 0.875:
        return "E7"
    elif energy > 0.875:
        return "E8"


def get_danceability(features):
    danceability = features.get("danceability")
    print(f"Dance: {danceability}")
    if danceability <= 0.125:
        return "D1"
    elif 0.125 < danceability <= 0.250:
        return "D2"
    elif 0.250 < danceability <= 0.375:
        return "D3"
    elif 0.375 < danceability <= 0.500:
        return "D4"
    elif 0.500 < danceability <= 0.625:
        return "D5"
    elif 0.625 < danceability <= 0.750:
        return "D6"
    elif 0.750 < danceability <= 0.875:
        return "D7"
    elif danceability > 0.875:
        return "D8"


def get_tempo(features):
    tempo = features.get("tempo")
    print(f"Tempo: {tempo}")
    if tempo < 70:
        return "T1"
    elif 70 < tempo <= 90:
        return "T2"
    elif 90 < tempo <= 110:
        return "T3"
    elif 110 < tempo <= 130:
        return "T4"
    elif 130 < tempo <= 150:
        return "T5"
    elif 150 < tempo <= 170:
        return "T6"
    elif 170 < tempo <= 190:
        return "T7"
    elif tempo > 190:
        return "T8"


def get_gradient(features):
    valence = color_palettes.get(get_valence(features))
    energy = color_palettes.get(get_energy(features))
    danceability = color_palettes.get(get_danceability(features))
    tempo = color_palettes.get(get_tempo(features))

    gradient = f"linear-gradient(45deg, {valence}, {energy}, {danceability}, {tempo})"
    return gradient
