import os

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


load_dotenv()


def get_secret_key():
    return os.getenv("SECRET_KEY")


def get_client(session):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT")

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id,
            client_secret,
            redirect_uri,
            scope="user-library-read",
            cache_handler=FlaskSessionCacheHandler(session),
        ),
        retries=5,
        requests_timeout=7,
    )

    return sp
