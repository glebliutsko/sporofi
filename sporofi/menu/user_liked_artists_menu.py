import typing

from sporofi.menu import Menu, Option, Key, ArtistTracksMenu, ArtistAlbumsMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class UserLikedArtistsMenu(Menu):
    PROMPT = 'album'

    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi'):
        super().__init__(spotify_client, rofi, {
            Key.USER_KEY_1: ('Alt+p', 'Play'),
            Key.USER_KEY_2: ('Alt+t', 'Show tracks')
        })

    def _generate_options(self) -> typing.List['Option']:
        def get_all_artists():
            last_id = None

            while True:
                page = self.spotify_client.current_user_followed_artists(50, last_id)['artists']

                if page['items'] != 0:
                    yield page['items']

                if page['cursors']['after']:
                    last_id = page['cursors']['after']
                else:
                    return

        options = []

        for page in get_all_artists():
            for artist in page:
                options.append(Option(
                    text=artist['name'],
                    keys={
                        Key.ENTER: Key(next_menu=ArtistAlbumsMenu, args=(artist['id'], )),
                        Key.USER_KEY_1: Key(callback=self._play_artist, args=(artist['id'], )),
                        Key.USER_KEY_2: Key(next_menu=ArtistTracksMenu, args=(artist['id'], ))
                    }
                ))

        return options

    def _play_artist(self, id_artist: str):
        artist_tracks = []

        for page_albums in get_all_page(self.spotify_client.artist_albums, artist_id=id_artist, limit=50,
                                        album_type='album,single,compilation'):
            for album in page_albums:
                for page_track in get_all_page(self.spotify_client.album_tracks, album_id=album['id'], limit=50):
                    for track in page_track:
                        artist_tracks.append(track['uri'])

        self.spotify_client.start_playback(uris=artist_tracks)
