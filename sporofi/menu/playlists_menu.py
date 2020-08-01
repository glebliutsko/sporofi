import typing

from sporofi.menu import Menu, Option, Key, LikedTracksMenu, PlaylistTracksMenu


class PlaylistsMenu(Menu):
    PROMPT = 'playlist'

    def _generate_options(self) -> typing.List[Option]:
        playlists = self.spotify_client.current_user_playlists()

        options = [Option(
            text='Liked songs',
            keys={Key.ENTER: Key(next_menu=LikedTracksMenu)}
        )]

        for playlist in playlists['items']:
            options.append(Option(
                text=playlist['name'],
                keys={Key.ENTER: Key(next_menu=PlaylistTracksMenu, args=(playlist['id'], ))}
            ))

        return options
