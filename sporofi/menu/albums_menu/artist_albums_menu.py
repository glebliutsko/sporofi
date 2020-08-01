import typing

from sporofi.menu import AlbumsMenu, Option, Key, AlbumTracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class ArtistAlbumsMenu(AlbumsMenu):
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi', id_artist: str):
        super().__init__(spotify_client, rofi)
        self.id_artist = id_artist

    def _get_albums(self) -> list:
        albums = []

        for page in get_all_page(self.spotify_client.artist_albums, limit=50, artist_id=self.id_artist,
                                 album_type='album,single,compilation'):
            for album in page:
                albums.append(album)

        return albums
