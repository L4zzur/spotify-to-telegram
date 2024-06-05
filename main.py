import time

import spotipy
from pyrogram import Client
from pyrogram.raw import functions
from spotipy.oauth2 import SpotifyOAuth

from config import (
    api_hash,
    api_id,
    client_id,
    client_secret,
    default_bio,
    is_premium,
    nowplay_bio,
    redirect_uri,
    scope,
    username,
)


def check_bio_len(bio_max_len: int, bio: str) -> str:
    """
    Returns truncated string and prints a warning if the string is truncated
    """
    if len(bio) > bio_max_len:
        print(
            f"Bio is too long! It's over the limit by {len(bio) - bio_max_len} characters."
        )
        return bio[: bio_max_len - 1][: bio.rfind(" ")] + "…"
    else:
        return bio


def update_status(app: Client, spotify: spotipy.Spotify, bio_max_len: int):
    global last_bio
    current_song = spotify.current_user_playing_track()

    if current_song is None or not current_song["is_playing"]:
        if last_bio != default_bio:
            print("None")
            last_bio = default_bio
            with app:
                app.invoke(functions.account.UpdateProfile(about=default_bio))
    else:
        track = current_song["item"]["name"]
        album = current_song["item"]["album"]["name"]
        artist = current_song["item"]["artists"][0]["name"]

        new_bio = check_bio_len(
            bio_max_len=bio_max_len,
            bio=nowplay_bio.substitute(artist=artist, track=track, album=album),
        )

        if last_bio != new_bio:
            last_bio = new_bio
            print(new_bio)
            with app:
                app.invoke(functions.account.UpdateProfile(about=new_bio))


if __name__ == "__main__":
    app = Client(name="spotify_to_bio", api_id=api_id, api_hash=api_hash)

    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            username=username,
            scope=scope,
        ),
        language="ru",
    )

    last_bio = None

    bio_max_len = 140 if is_premium else 70

    try:
        while True:
            try:
                update_status(app=app, spotify=spotify, bio_max_len=bio_max_len)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting...\n")
        exit()
