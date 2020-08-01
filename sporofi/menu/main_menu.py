import typing

from sporofi.menu import Menu, Option, Key, UserPlaylistsMenu, UserLikedArtistsMenu, UserLikedAlbumsMenu


class MainMenu(Menu):
    def _generate_options(self) -> typing.List['Option']:
        return [
            Option(
                text='Playlists',
                keys={Key.ENTER: Key(next_menu=UserPlaylistsMenu)}
            ),
            Option(
                text='Artists',
                keys={Key.ENTER: Key(next_menu=UserLikedArtistsMenu)}
            ),
            Option(
                text='Albums',
                keys={Key.ENTER: Key(next_menu=UserLikedAlbumsMenu)}
            )
        ]
