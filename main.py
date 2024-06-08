import spotipy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from httpx import AsyncClient
from loguru import logger
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message
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

try:
    from config import (
        chat_id,
        default_message,
        message_id,
        nowplay_message,
        use_channel_nowplay,
    )
except ImportError:
    use_channel_nowplay = False


def check_bio_len(max_bio_len: int, bio: str) -> str:
    """Checks if bio is too long and truncates it

    Args:
        max_bio_len (int): maximum length of the bio
        bio (str): current bio

    Returns:
        str: truncated bio and logs a warning if the bio is too long
    """
    if len(bio) > max_bio_len:
        logger.warning(
            f"Bio is too long!"
            f"It's over the limit by {len(bio) - max_bio_len} characters."
        )
        return bio[: max_bio_len - 1][: bio.rfind(" ")] + "…"
    else:
        return bio


async def update_status(app: Client, spotify: spotipy.Spotify, max_bio_len: int):
    """Updates the status of the user

    Args:
        app (Client): Pyrogram client
        spotify (spotipy.Spotify): Spotify client
        max_bio_len (int): maximum length of the bio
    """

    global last_bio
    current_song = spotify.current_user_playing_track()

    if current_song is None or not current_song["is_playing"]:
        if last_bio != default_bio:
            logger.info("Nothing playing")
            last_bio = default_bio
            await app.update_profile(bio=default_bio)
    else:
        track = current_song["item"]["name"]
        album = current_song["item"]["album"]["name"]
        artist = current_song["item"]["artists"][0]["name"]

        new_bio = check_bio_len(
            max_bio_len=max_bio_len,
            bio=nowplay_bio.substitute(artist=artist, track=track, album=album),
        )

        if last_bio != new_bio:
            last_bio = new_bio
            logger.info(new_bio)
            await app.update_profile(bio=new_bio)


async def create_message(spotify: spotipy.Spotify) -> str:
    """Creates a message based on the current song

    Args:
        spotify (spotipy.Spotify): Spotify client

    Returns:
        str: Message with now playing information with links
    """
    current_song = spotify.current_user_playing_track()

    if current_song is None or not current_song["is_playing"]:
        return default_message
    else:
        track = current_song["item"]["name"]
        album = current_song["item"]["album"]["name"]
        artist = current_song["item"]["artists"][0]["name"]
        url = current_song["item"]["external_urls"]["spotify"]
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    url="https://songwhip.com/" + url, follow_redirects=True
                )
                other_url = response.url
        except Exception:
            other_url = "Error"

        new_message = nowplay_message.substitute(
            artist=artist, track=track, album=album, spotify=url, other=other_url
        )
        return new_message


async def update_message(
    app: Client, spotify: spotipy.Spotify, chat_id: int, message_id: int
) -> None:
    """Updates the message with the current song

    Args:
        app (Client): Pyrogram client
        spotify (spotipy.Spotify): Spotify client
        chat_id (int): Chat ID
        message_id (int): Message ID
    """
    text = await create_message(spotify=spotify)

    try:
        await app.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=str(text),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    except MessageNotModified:
        pass


async def send_message(message: Message) -> None:
    """Sends a message with the current song

    Args:
        message (Message): Telegram message to edit
    """
    global spotify
    text = await create_message(spotify=spotify)

    await message.edit_text(
        text=str(text),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


if __name__ == "__main__":
    logger.info("Starting Pyrogram...")
    app = Client(name="spotify_to_bio", api_id=api_id, api_hash=api_hash)

    logger.info("Starting Spotify...")
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
    max_bio_len = 140 if is_premium else 70

    nowplay_handler = MessageHandler(
        callback=send_message,
        filters=(filters.command("nowplay", "!")),
    )
    app.add_handler(nowplay_handler)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=update_status,
        kwargs={
            "app": app,
            "spotify": spotify,
            "max_bio_len": max_bio_len,
        },
        trigger="interval",
        seconds=15,
    )

    if use_channel_nowplay:
        scheduler.add_job(
            func=update_message,
            kwargs={
                "app": app,
                "spotify": spotify,
                "chat_id": chat_id,
                "message_id": message_id,
            },
            trigger="interval",
            seconds=20,
        )

    scheduler.start()
    app.run()

    # try:
    #     while True:
    #         try:
    #             update_status(app=app, spotify=spotify, max_bio_len=max_bio_len)
    #         except Exception as e:
    #             logger.error(f"Произошла ошибка: {e}")
    #         time.sleep(5)
    # except KeyboardInterrupt:
    #     print("\nExiting...\n")
    #     exit()
