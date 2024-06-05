import spotipy
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from spotipy.oauth2 import SpotifyOAuth
from config import api_hash, api_id, client_id, client_secret, redirect_uri, username, scope, status
telethon_client = TelegramClient('anon', api_id, api_hash).start()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        username=username,
        scope=scope,
    ),
    language='ru'
)

def update_status():
    global last_status
    current = spotify.current_user_playing_track()
    if current is None or not current['is_playing']:
        if last_status != status:
            print("None")
            last_status = status
            telethon_client(UpdateProfileRequest(about=status))
    else:
        track = current["item"]["name"]
        album = current["item"]["album"]["name"]
        artist = current["item"]["artists"][0]["name"]
        music = '🎧 Now Playing | ' + artist + ' - ' + track
        if len(music) > 70:
            music = music[:69][:music.rfind(' ')] + '…'
        if last_status != music:
            last_status = music
            print(music)
            telethon_client(UpdateProfileRequest(about=music))

if __name__ == '__main__':
    last_status = None
    while True:
        try:
            update_status()
        except Exception as e:
            print(f'Произошла ошибка: {e}')
        time.sleep(5)