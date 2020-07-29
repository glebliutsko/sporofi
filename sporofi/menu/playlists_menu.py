import typing

from sporofi.menu import Menu, Option, LikedTracksMenu, PlaylistTracksMenu


class PlaylistsMenu(Menu):
    def _generate_options(self) -> typing.List[Option]:
        playlists = self.spotify_client.current_user_playlists()

        options = [Option(
            text='Liked songs',
            next_menu=LikedTracksMenu,
            args=()
        )]

        for playlist in playlists['items']:
            options.append(Option(
                text=playlist['name'],
                next_menu=PlaylistTracksMenu,
                args=(playlist['id'], )
            ))

        return options
