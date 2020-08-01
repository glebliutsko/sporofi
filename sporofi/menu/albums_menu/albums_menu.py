import typing

from sporofi.menu import Menu, Option, Key, AlbumTracksMenu

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class AlbumsMenu(Menu):
    PROMPT = 'album'

    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi'):
        super().__init__(spotify_client, rofi, {
            Key.USER_KEY_1: ('Alt+p', 'Play')
        })

    def _get_albums(self) -> list:
        raise NotImplemented

    def _generate_options(self) -> typing.List['Option']:
        options = []

        for album in self._get_albums():
            options.append(Option(
                text=f'{album["artists"][0]["name"]} - {album["name"]}',
                keys={
                    Key.ENTER: Key(next_menu=AlbumTracksMenu, args=(album['id'], )),
                    Key.USER_KEY_1: Key(callback=self._play_album, args=(album['uri'], ))
                }
            ))

        return options

    def _play_album(self, uri_album):
        self.spotify_client.start_playback(context_uri=uri_album)
