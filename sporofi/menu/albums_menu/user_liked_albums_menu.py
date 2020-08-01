from sporofi.menu import AlbumsMenu
from sporofi.utils import get_all_page


class UserLikedAlbumsMenu(AlbumsMenu):
    def _get_albums(self) -> list:
        albums = []

        for page in get_all_page(self.spotify_client.current_user_saved_albums, limit=50):
            for album in page:
                albums.append(album['album'])

        return albums
