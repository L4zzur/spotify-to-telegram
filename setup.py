import gettext
import os

from jinja2 import Environment, FileSystemLoader
from pyrogram.client import Client

lang = input("Choose language (ru/en): ").lower()
if lang not in ["ru", "en"]:
    print("Wrong language")
    exit()

translations = gettext.translation(
    domain="messages", localedir="translations/", languages=[lang]
)
translations.install()  # Magically make the _ function globally available
_ = translations.gettext

# Telegram
print(_("------ Setting up Telegram ------"))
print(_("Please enter the following details"))
api_id = int(input(_("Enter API ID: ")))  # my.telegram.org
api_hash = input(_("Enter API Hash: "))  # my.telegram.org
if input(_("Do you want to set up Now Playing for a your bio? (y/n): ")) == "y":
    use_bio_nowplay = True
    is_premium = True if input(_("Your account has Premium? (y/n): ")) == "y" else False
    default_bio = input(_("Enter default bio: "))
    print()
else:
    use_bio_nowplay = False
    is_premium = False
    default_bio = None

#  Telegram Channel Message
if (
    input(_("Do you want to set up Now Playing for a message in your channel? (y/n): "))
    == "y"
):
    use_channel_nowplay = True
    chat_id = int(input(_("Enter chat ID: ")))
    message_id = int(input(_("Enter message ID: ")))
    account = input(_("Enter account URL (you can use bit.ly): "))
    default_message = input(_("Enter default message: "))
    print()
else:
    use_channel_nowplay = False
    chat_id = None
    message_id = None
    account = None
    default_message = None


# Spotify
print(_("------ Setting up Spotify ------"))
print(_("Please enter the following details"))
client_id = input(_("Enter Client ID: "))  # developer.spotify.com/dashboard
client_secret = input(_("Enter Client Secret: "))  # developer.spotify.com/dashboard
username = input(_("Enter username: "))
redirect_uri = "http://localhost:8888/callback"  # Don't touch
scope = "user-read-currently-playing"
print(_("Setup completed!"))

config_data = {
    "api_id": api_id,
    "api_hash": api_hash,
    "use_bio_nowplay": use_bio_nowplay,
    "is_premium": is_premium,
    "default_bio": default_bio,
    "use_channel_nowplay": use_channel_nowplay,
    "chat_id": chat_id,
    "message_id": message_id,
    "account": account,
    "default_message": default_message,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "username": username,
    "scope": scope,
}

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("config.j2")

config = template.render(config_data)

with open("config.py", "w", encoding="utf-8") as f:
    f.write(config)

for file in os.listdir():
    if file.endswith(".session") or file.endswith(".session-journal"):
        os.remove(file)

print("Login to your Telegram account")
app = Client(name="spotify_to_bio", api_id=api_id, api_hash=api_hash)
app.run()
