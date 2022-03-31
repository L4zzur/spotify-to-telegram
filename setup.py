config = open('config.py', 'w')
lang = input('Выберите язык / Choose language (RU  EN): ')
if lang.lower() == 'ru':
    from russian import *
elif lang.lower() == 'en':
    from english import *
else:
    print('Выбран неверный язык / The wrong language is selected')
    exit()

# Telegram
print(tg_start1)
print(tg_start2)
api_id = input(api_id_text) # my.telegram.org
api_hash = input(api_hash_text) # my.telegram.org
status = input(status_text)
config.write(f'# Telegram\napi_id = {api_id}\napi_hash = "{api_hash}"\nstatus = "{status}"\n# Spotify\n')

# Spotify
print(spotify_start1)
print(spotify_start2)
client_id = input(client_id_text)
client_secret = input(client_secret_text)
redirect_uri = "http://localhost:8888/callback" # Не трогать / Don't touch
username = input(username_text)
scope = 'user-read-currently-playing'
config.write(f'client_id = "{client_id}"\nclient_secret = "{client_secret}"\nredirect_uri = "{redirect_uri}"\nusername = "{username}"\nscope = "{scope}"')
config.close()
print(final_text, f'\nhttps://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope=user-read-currently-playing&redirect_uri=http://localhost:8888/callback')