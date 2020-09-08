#!/usr/bin/python
import argparse
import json
import os

import rofi
from spotipy import Spotify, SpotifyOAuth

from sporofi.menu import MainMenu, ControlMenu, ArtistTracksMenu, UserPlaylistsMenu, UserLikedAlbumsMenu,\
    LikedTracksMenu
from sporofi.exception import UserCancel


def get_dir_conf():
    parent_config_dir = os.getenv('XDG_CONFIG_HOME')
    if not parent_config_dir:
        parent_config_dir = os.getenv('HOME')
    if not parent_config_dir:
        parent_config_dir = os.getenv('./')

    config_dir = os.path.join(parent_config_dir, 'sporofi')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    return config_dir


DIR_CONF = get_dir_conf()


def setup():
    client_id = input('Client ID: ')
    client_secret = input('Client secret: ')

    with open(os.path.join(DIR_CONF, 'client.json'), 'w') as f:
        json.dump(
            {'client_id': client_id, 'client_secret': client_secret},
            f,
            indent=4
        )


def get_client_conf() -> dict:
    with open(os.path.join(DIR_CONF, 'client.json')) as f:
        return json.load(f)


modes = {
    'main': MainMenu,
    'control': ControlMenu,
    'artists': ArtistTracksMenu,
    'albums': UserLikedAlbumsMenu,
    'tracks': LikedTracksMenu,
    'playlists': UserPlaylistsMenu,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', action='store_true', default=False)
    parser.add_argument('--mode', '-m', default=list(modes)[0], choices=modes.keys())

    args = parser.parse_args()

    if args.setup:
        setup()
    else:
        client_conf = get_client_conf()
        oauth = SpotifyOAuth(
            client_id=client_conf['client_id'],
            client_secret=client_conf['client_secret'],
            redirect_uri='http://localhost:8080/',
            scope='user-modify-playback-state app-remote-control streaming user-read-playback-state user-library-read',
            cache_path=os.path.join(DIR_CONF, 'auth.json')
        )
        sp = Spotify(oauth_manager=oauth)
        rofi_client = rofi.Rofi(rofi_args=['-i'])

        try:
            modes[args.mode](sp, rofi_client).run()
        except UserCancel:
            print('Cancel...')


if __name__ == '__main__':
    main()
