import typing

from sporofi.menu import TracksMenu
from sporofi.utils import get_all_page


class LikedTracksMenu(TracksMenu):
    @property
    def _context(self) -> typing.Union[str, None]:
        return None

    def _get_tracks(self) -> dict:
        liked_tracks = {}

        for page in get_all_page(self.spotify_client.current_user_saved_tracks):
            for track in page:
                liked_tracks[track['track']['uri']] = \
                    f"{track['track']['artists'][0]['name']} - {track['track']['name']}"

        return liked_tracks
