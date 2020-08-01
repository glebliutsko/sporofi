import typing

from sporofi.menu import TracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class PlaylistTracksMenu(TracksMenu):
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi', id_playlist: str):
        super().__init__(spotify_client, rofi)
        self.id_playlist = id_playlist

    @property
    def _context(self) -> typing.Union[str, None]:
        return f'spotify:playlist:{self.id_playlist}'

    def _get_tracks(self) -> list:
        tracks = []

        for page in get_all_page(self.spotify_client.playlist_tracks, limit=100, playlist_id=self.id_playlist):
            for track in page:
                tracks.append(track['track'])

        return tracks
