# Audiodive V2

from dataclasses import dataclass
import requests

from flask import Flask, redirect, session, url_for, jsonify, render_template

from auth import get_client, get_secret_key
from helpers import *
from search import SpotifySearch


app = Flask(__name__)
app.secret_key = get_secret_key()
app.config["SESSION_COOKIE_NAME"] = "galleta_musical"

sp = get_client(session)
search = SpotifySearch(sp)


@app.route("/login")
def login():
    sp_oauth = get_client(session).auth_manager
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    sp_oauth = get_client(session).auth_manager
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    user_info = sp.current_user()
    user_id = user_info["id"]
    session["user_id"] = user_id
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("token_info", None)
    session.clear()
    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("index.html", session=session)


@app.route("/search", methods=["GET"])
def search_suggestions():
    query = request.args.get("q", "")
    if query:
        try:
            results = search.search(query)
            suggestions = process_search_results(results)
            return jsonify(suggestions)
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify([])


@dataclass
class TrackDetails:
    track_id: str
    key: str
    bpm: float
    loudness: float
    gradient: float
    image: str
    genres: list
    related_artists: list
    data: dict


@app.route("/result/<track_id>")
def show_result(track_id):
    try:
        data = search.get_track_data(track_id)
        features = data["features"][0]

        track_details = TrackDetails(
            track_id=track_id,
            key=get_key_signature(features),
            bpm=get_bpm(features),
            loudness=get_loudness(features),
            gradient=get_gradient(features),
            image=get_artist_image(track_id),
            genres=get_artist_genre(track_id),
            related_artists=get_related_artists(track_id),
            data=data,
        )

        return render_template("result.html", track_details=track_details)

    except Exception as e:
        app.logger.error(f"Error retrieving track data: {e}")
        return render_template("error.html")


@app.route("/random", methods=["POST"])
def random():
    track_id = random_track()
    return redirect(url_for("show_result", track_id=track_id))


@app.route("/recommend", methods=["POST"])
def recommend():
    track_id = request.form.get("track_id")
    new_track_id = get_new_track(track_id)
    return redirect(url_for("show_result", track_id=new_track_id))


@app.template_filter("format_mmss")
def format_mmss(duration_ms):
    ms = duration_ms / 1000
    minutes = int(ms // 60)
    seconds = int(ms % 60)
    return f"{minutes:02}:{seconds:02}"


if __name__ == "__main__":
    app.run
