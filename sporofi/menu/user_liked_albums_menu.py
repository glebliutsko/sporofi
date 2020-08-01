import typing

from sporofi.menu import Menu, Option, Key, AlbumTracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class UserLikedAlbumsMenu(Menu):
    PROMPT = 'album'

    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi'):
        super().__init__(spotify_client, rofi, {
            Key.USER_KEY_1: ('Alt+p', 'Play')
        })

    def _generate_options(self) -> typing.List['Option']:
        options = []

        for page in get_all_page(self.spotify_client.current_user_saved_albums, limit=50):
            for album in page:
                options.append(Option(
                    text=f'{album["album"]["artists"][0]["name"]} - {album["album"]["name"]}',
                    keys={
                        Key.ENTER: Key(next_menu=AlbumTracksMenu, args=(album['album']['id'], )),
                        Key.USER_KEY_1: Key(callback=self._play_album, args=(album['album']['uri'], ))
                    }
                ))

        return options

    def _play_album(self, uri_album):
        self.spotify_client.start_playback(context_uri=uri_album)
