import spotipy
from spotipy.exceptions import SpotifyException


class SpotifySearch:
    def __init__(self, sp):
        self.sp = sp

    def search(self, query, search_type="track,artist"):
        results = self.sp.search(q=query, type=search_type, limit=10)
        return results

    def random_search(self, query, search_type="track", market=None):
        results = self.sp.search(q=query, type=search_type, market=market, limit=33)
        return results

    def get_track(self, track_id):
        track = self.sp.track(track_id)
        return track

    def get_features(self, track_id):
        features = self.sp.audio_features(tracks=[track_id])
        return features

    def get_analysis(self, track_id):
        analysis = self.sp.audio_analysis(track_id)
        return analysis

    def get_track_data(self, track_id):
        track = self.get_track(track_id)
        features = self.get_features(track_id)
        analysis = self.get_analysis(track_id)
        return {
            "track": track,
            "track_id": track_id,
            "features": features,
            "analysis": analysis,
        }

    def get_artist_id(self, track_id):
        track_data = self.get_track_data(track_id)
        artist_id = track_data["track"]["artists"][0]["id"]
        return artist_id

    def get_artist_data(self, artist_id):
        results = self.sp.artist(artist_id)
        return results

    def get_track_recommendation(self, track_id):
        try:
            track = self.sp.recommendations(
                seed_tracks=[track_id], limit=1, max_popularity=50
            )
            return track
        except Exception as e:
            print("Method - Error fetching recommendation:", e)
            return None

    def get_related_artists(self, track_id):
        artist_id = self.get_artist_id(track_id)
        related_artists = self.sp.artist_related_artists(artist_id)
        return related_artists
