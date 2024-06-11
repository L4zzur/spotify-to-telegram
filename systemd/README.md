# Install on Linux Server (VPS/VDS)

## Pre-requisites
Read [README.md](README.md) for installation instructions. 
You need the files `*tg-app-name*.session` and `.cache-*spotify username*`.

## Install on VPS/VDS
>Check that the Python version is at least 3.11. On the versions below, the work is not guaranteed, but you can check and notify me about it.

###### Clone the repository:
```bash
$ git clone https://github.com/L4zzur/spotify-to-telegram.git
```

###### Go to the "spotify-to-telegram" folder:
```bash
$ cd spotify-to-telegram
```

###### Create a virtual environment and activate it:
```bash
$ python -m venv venv
$ source venv/bin/activate
```

###### Install libraries using pip:
```bash
$ pip install -r requirements.txt
```

## Setting up

### Files
Transfer your locally received files `*tg-app-name*.session` and `.cache-*spotify username*` to the cloned directory on your VPS/VDS.

### Systemd
You need to copy the `spotifytotelegram.service` file into the `/etc/systemd/system` folder on your VPS/VDS.

### Run
Start the service using `sudo systemctl start spotifytotelegram.service`. 

## Possible problems
After changing the password in Spotify or deleting the active session for the Telegram script, you need to get new files locally again and move them to VPS/VDS.

After these steps you need to restart the service by `sudo systemctl restart spotifytotelegram.service`.