# sporofi
Rofi wrapper for spotify
![sporofi](https://user-images.githubusercontent.com/40576167/92515434-a89fa280-f224-11ea-8b66-6b716b49a575.png)


## Installing
```bash
pip install -r requirements.txt
# or
virtualenv venv
pip install -r requirements.txt
```

## Setup
1. Create app to [Spotify dashboard](https://developer.spotify.com/dashboard/applications)
2. Add `http://localhost:8080/` to Redirect URIs
3. Run `python -m sporofi --setup`
4. Enter `Client ID`
5. Enter `Client secret`
6. The first time you use it, you will be redirected to the official Spotify web page to ask for your permissions.

Your config store in `$XDG_CONFIG_HOME/.config/sporofi`

## Usage
`python -m sporofi --mode [mode]`

Modes:
 - main
 - control
 - artists
 - albums
 - tracks
 - playlists
