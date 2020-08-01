import typing

from sporofi.menu import AlbumsMenu, Option, Key, AlbumTracksMenu
from sporofi.utils import get_all_page

if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class UserLikedAlbumsMenu(AlbumsMenu):
    def _get_albums(self) -> list:
        albums = []

        for page in get_all_page(self.spotify_client.current_user_saved_albums, limit=50):
            for album in page:
                albums.append(album)

        return albums
