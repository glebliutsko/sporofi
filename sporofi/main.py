#!/usr/bin/python
import argparse
import json
import os

import rofi
from spotipy import Spotify, SpotifyOAuth
from spotipy.exceptions import SpotifyException

from sporofi.menu import UserLikedAlbumsMenu, ArtistAlbumsMenu, UserLikedArtistsMenu, AlbumTracksMenu, ArtistTracksMenu, \
    LikedTracksMenu, PlaylistTracksMenu
from sporofi.exception import UserCancel

# DIR_CONF = '$HOME/.config/sporofi/'
DIR_CONF = './'


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-dir')
    parser.add_argument('--setup', help='Initial configuration', action='store_true', default=False)
    parser.add_argument('--mode', help='Initial configuration', choices=['Control'], default=False)

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
            PlaylistTracksMenu(sp, rofi_client, '0vsOloA6zIaPqjWz3RRyE4').run()
        except UserCancel:
            print('Cancel...')


if __name__ == '__main__':
    main()
