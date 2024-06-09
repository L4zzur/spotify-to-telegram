from string import Template

# Telegram
api_id = 1000000
api_hash = ""
is_premium = True

#  Telegram Bio
use_bio_nowplay = True
default_bio = "Default Bio"
nowplay_bio = Template("🎧 Now Playing: $artist — $track")

#  Telegram Channel Message
use_channel_nowplay = True
chat_id = -1000000000000
message_id = 100
account = "https://spoti.fi/"
default_message = f"Currently not playing | [Spotify Account]({account})"
nowplay_message = Template(
    f"🎧 Now Playing: $artist — $track — $album\n"
    f"[▶️ Spotify]($spotify) | [🔗 Other]($other) | [Spotify Account]({account})"
)

# Spotify
client_id = ""
client_secret = ""
username = ""
redirect_uri = "http://localhost:8888/callback"
scope = "user-read-currently-playing"
