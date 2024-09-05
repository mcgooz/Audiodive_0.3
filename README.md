# Audiodive
## Video Demo: TBC
## Description:
Audiodive is a web app that utilises the Spotify API (via Spotipy) to allow users to search for and play tracks in their browser. A Spotify user account is required for full functionality. 

What sets this app apart is the inclusion of several features that are not readily available on Spotify, neither via the app nor the desktop application. In addition to an embedded spotify web-player, Audiodive also provides hidden details relating to each track, such as key, tempo, loudness, and popularity. You can also choose to play a similar track by using the 'Find a Similar Track' button.

An additional, subtle, yet pleasing feature is the changing background. Based on Spotify's values for valence (happy or sad), energy, danceability and tempo, each track features a distinct colour palette that will slowly evolve as you listen.

The last (and potentially most fun) feature is the ability to get a random track at the click of a button. More details below.

### Technical Details
Audiodive is a web app that fetches a range of data from the Spotify web API via the Python library, Spotipy. The front end is rendered using a combination of HTML, CSS and some JavaScript with the helping hand of Bootstrap 5 to allow for a professional, responsive design. The backend is written in Python with Jinja used to pass information to the HTML templates.

#### Functionality
##### Python
- *app.py* is the principal file that manages the set-up, routing, requests and running of the app server.
- *auth.py* takes care of the Spotify authentication, allowing the user to log in to Spotify. After authentication, the app creates a local session so that logging in and out can be handled manually.
- *search.py*: Using the Spotipy library, *search.py* defines a SpotifySearch class and several methods that can pull data from the Spotify API, such as track details, audio features, track recommendations, and so on.
- *helpers.py* is where the main under-the-hood functionality lies. This file calls on the SpotifySearch class to then extract the finer details from the search results. For example:
    ```
    def get_loudness(features):
        loudness = features.get("loudness")
        return f"{loudness:.1f} dB"
    ```   
    Another more complex example, the random track function, passes a string consisting of a random character with the wildcard search symbol ("%") and a randomly selected market, as a kwarg, to the random search method. This method returns a list of 33 track IDs from which the helper function then randomly picks one and passes it to the Spotify web player in the front end.   
    Although this seems pretty fool-proof, the Spotify algorithm still insists on pushing the same collection of tracks, no matter how much you try to randomise. That said, after several unsuccessful attempts at convincing Spotify that 100% reggaeton is not random(!), I'm reasonably happy with how well this feature evades its attempts (most of the time) and you're likely to find some pretty "interesting" music out there!   

        ```
        def random_search(self, query, search_type="track", market=None):
            try:
                results = self.sp.search(q=query, type=search_type, market=market, limit=33)
                return results

            except SpotifyException as e:
                self.log_status(e.http_status, e.code, e.msg, e.reason, e.headers)
                raise e
        ```

    ```
    random_char = random.choice(chars)
    random_market = random.choice(markets)
    extra_random = random.choice(wildcard)
    query = extra_random + random_char + "%"

    random_result = search.random_search(
        query, search_type="track", market=random_market
    )
    track_id = [track["id"] for track in random_result["tracks"]["items"]]
    random_track = random.choice(track_id)
    return random_track
    ```
    Other functions include getting the key and mode (major or minor), which the have to be combined before being passed to the front-end, retrieving the artist's genres, and, of course, the valence, energy, danceability and tempo to be able to create the shifting gradient background.

- *color_palettes.py* is simply a dictionary that contains a palette of HTML colour codes that correspond to the results (provided as decimals between 0 -1, except tempo) of valence, energy, danceability and tempo. In another helper function, the relevant colours are then combined into a css string and passed to the results.html page to be rendered:

    `gradient = f"linear-gradient(45deg, {valence}, {energy}, {danceability}, {tempo})"`

##### HTML
Next we have the HTML files. Each page has a fixed navigation bar that includes the app logo and (once the user is logged in) a "Logout" button:
- *index.html* is where you can search for a track or try your luck with the random track button.   

- *layout.html* implements the overall structure of each page, rendering the navbar, footer and, of course, Spotify attribution.   

- *login.html* is the first page we see if we're not logged in, and it simply prompts us to log in via Spotify. This button will redirect you to the Spotify login page and then return you to *index.html*.   

- Lastly, we have *result.html*. This is where you'll find your search result with all the juicy details, an embedded Spotify web player, and the evolving colourful background. There's also a pair of buttons to let you find a similar track or try another random track.

##### Static Files
The static folder contains assests, CSS and a short JavaScript file.
- *script.js* implements certain subtle front-end elements: When searching, an event listener will trigger the process of fetching, finding and displaying a dropdown of auto-suggestions will appear. Another script will then, in turn, disable the highlight around the search box. Lastly, there's a script to detect valid or invalid input. If the input is valid, the query will be passed to *app.py* in order to then load *results.html*. If the query is invalid, a pop-up will display a message that a valid search is required.
- *styles.css* contains some CSS that is necessary on top of the style elements provided by Bootstrap.
- The remaining files are images, logos, fonts and icons. 

### Challenges
- Authorisation and logins: This was my first real experience of implementing an authorisation flow and, yes, it was difficult. As a beginner, I found both the Spotipy and Spotify API documentation to be relatively cryptic and had to turn to the CS50 duck almost every step of the way. Now that I have the log in/log out working and on paper, so to speak, I think I have taken a huge step to understanding the routing, callbacks and so on.   

- Timeouts and rate limits: The Spotify API supposedly returns a 429 when you have made too many requests, with a number in the header advising you of how long, in seconds, to back-off for. Unfortunately, this isn't carried forward (as far as I can tell) by the Spotipy library which resulted in me getting a "MAX LIMIT EXCEEDED" error, effectively meaning I had to wait around 12 hours before I could make API calls again. The worst part was that, before I reached this limit, app functionality started to suffer, with track recommendations no longer working, or searches just hanging indefinitely causing me to think it was my code that was broken, when in fact, it was just the 429 telling me to back off. Well, I've learnt my lesson!   

- Colours for the colour palette: I'm colour-blind, so matching different shades of red, orange, green etc with decimal values was too much of a challenge for me. It turns out that ChatGPT shares the same deficiency! Countless times I provided a prompt such as "Could you give me the html colour code for soft orange", only to recieve the code for what turned out to be green! 


#### Improvements
In future updates, I hope to include:
- An autoplay toggle; automating the "Find a Similar Track" and/or random track functionality.
- Extra colours for the mood palette, linked to other parameters in the audio feature set, such as "acousticness".
- Playlist creation and organisation as well as listening history; most likely using SQL to maintain the database.
- A visual indicator for the popularity result rather than a percentage.

##### I hope you enjoy diving into a new way of listening to music!
