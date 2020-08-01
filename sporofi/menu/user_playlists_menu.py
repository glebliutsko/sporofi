import typing

from sporofi.menu import Menu, Option, Key, LikedTracksMenu, PlaylistTracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class UserPlaylistsMenu(Menu):
    PROMPT = 'playlist'

    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi'):
        super().__init__(spotify_client, rofi, {
            Key.USER_KEY_1: ('Alt+p', 'Play')
        })

    def _generate_options(self) -> typing.List[Option]:
        playlists = self.spotify_client.current_user_playlists()

        options = [Option(
            text='Liked songs',
            keys={
                Key.ENTER: Key(next_menu=LikedTracksMenu),
                Key.USER_KEY_1: Key(callback=self._play_liked_song)
            }
        )]

        for playlist in playlists['items']:
            options.append(Option(
                text=playlist['name'],
                keys={
                    Key.ENTER: Key(next_menu=PlaylistTracksMenu, args=(playlist['id'], )),
                    Key.USER_KEY_1: Key(callback=self._play_playlist, args=(playlist['uri'], ))
                }
            ))

        return options

    def _play_liked_song(self):
        uris_tracks = []

        for page in get_all_page(self.spotify_client.current_user_saved_tracks, limit=50):
            for track in page:
                uris_tracks.append(track['track']['uri'])

        self.spotify_client.start_playback(uris=uris_tracks)

    def _play_playlist(self, uri_playlist):
        self.spotify_client.start_playback(context_uri=uri_playlist)
