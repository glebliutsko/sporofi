import typing

from sporofi.menu import TracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class AlbumTracksMenu(TracksMenu):
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi', id_album: str):
        super().__init__(spotify_client, rofi)
        self.id_album = id_album

    @property
    def _context(self) -> typing.Union[str, None]:
        return f'spotify:album:{self.id_album}'

    def _get_tracks(self) -> dict:
        album_tracks = {}

        for page_track in get_all_page(self.spotify_client.album_tracks, album_id=self.id_album, limit=50):
            for track in page_track:
                album_tracks[track['uri']] = f'{track["name"]}'

        return album_tracks
