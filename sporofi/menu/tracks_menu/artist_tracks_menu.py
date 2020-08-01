import typing

from sporofi.menu import TracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class ArtistTracksMenu(TracksMenu):
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi', id_artist: str):
        super().__init__(spotify_client, rofi)
        self.id_artist = id_artist

    @property
    def _context(self) -> typing.Union[str, None]:
        return f'spotify:artist:{self.id_artist}'

    def _get_tracks(self) -> dict:
        artist_tracks = {}

        for page_albums in get_all_page(self.spotify_client.artist_albums, artist_id=self.id_artist, limit=50,
                                        album_type='album,single,compilation'):
            for album in page_albums:
                for page_track in get_all_page(self.spotify_client.album_tracks, album_id=album['id'], limit=50):
                    for track in page_track:
                        artist_tracks[track['uri']] = f'{album["name"]} - {track["name"]}'

        return artist_tracks

