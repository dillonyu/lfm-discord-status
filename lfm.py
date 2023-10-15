import time

import urllib
from pypresence import Presence
import requests

# Constants
LASTFM_API_KEY = 'YOUR_API_KEY'
LASTFM_USERNAME = 'YOUR_LASTFM_USERNAME'
DISCORD_APP_ID = 'YOUR_DISCORD_APP_ID'  # You get this from your Discord application

# Initialize Discord Rich Presence
RPC = Presence(DISCORD_APP_ID)
RPC.connect()

while True:
    # Fetch the current song from Last.fm
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LASTFM_USERNAME}&api_key={LASTFM_API_KEY}&format=json")
    data = response.json()

    if 'recenttracks' in data and 'track' in data['recenttracks']:
        track = data['recenttracks']['track'][0]
        artist = track['artist']['#text']
        song_name = track['name']

        # Check if the song is currently being played
        is_now_playing = track.get('@attr', {}).get('nowplaying') == 'true'

        if is_now_playing:
            # URL encode artist and song name for the Last.fm URL
            encoded_artist = urllib.parse.quote_plus(artist)
            encoded_song_name = urllib.parse.quote_plus(song_name)

            # Extract album art URL
            album_art_url = track['image'][-1]['#text'] if track['image'] else 'https://cdn.icon-icons.com/icons2/2592/PNG/512/lastfm_logo_icon_154484.png'

            # Fetch total scrobbles for the track
            scrobble_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&user={LASTFM_USERNAME}&track={song_name}&artist={artist}&api_key={LASTFM_API_KEY}&format=json")
            scrobble_data = scrobble_response.json()
            total_scrobbles = scrobble_data['track']['userplaycount'] if 'track' in scrobble_data and 'userplaycount' in scrobble_data['track'] else "0"

            # Create the URL for the song page on Last.fm
            song_page_url = f"https://www.last.fm/music/{encoded_artist}/_/{encoded_song_name}"

            # Create the URL for the user's Last.fm profile
            profile_url = f"https://www.last.fm/user/{LASTFM_USERNAME}"
            
            # Update Discord status with button displaying total scrobbles
            RPC.update(
                details=song_name, 
                state="by " + artist, 
                large_image=album_art_url,
                small_image='lastfm',
                buttons=[{"label": f"Dill's Scrobbles: {total_scrobbles}", "url": song_page_url},
                         {"label": "View My Last.fm Profile", "url": profile_url}]
            )
    time.sleep(10)  # Check every 10 seconds
