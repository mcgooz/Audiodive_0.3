# Audiodive

## Update 27/11/24
Spotify has announced that a number of API endpoints, that this app depends on, are no longer available. Therefore, for the time being, Audiodive is non-functional :(

## Description:
Audiodive is a web app that utilises the Spotify API (via Spotipy) to search for and play tracks, adding additional details and aesthetics that aren't found in the Spotify mobile or desktop apps. 

Currently still in dev stage, a Spotify developer account is required for full functionality.

### Setup
Register the app on Spotify for Developers.
Add an .env file to the parent directory with your own secret key and then Spotify developer credentials:
```
SECRET_KEY= "secretkeygoeshere"
CLIENT_ID = "SpotifyIDgoeshere"
CLIENT_SECRET = "Spotifysecretgoeshere"
REDIRECT = "redirectURIgoeshere"
```

### Usage
Run Flask server from the terminal:
> $ flask run

Open the app in browser, click the Log In button to log in to your Spotify account (regular user account). You'll then be redirected to the Audiodive homepage. Crank the volume (optional).