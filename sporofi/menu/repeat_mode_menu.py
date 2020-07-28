import typing

from sporofi.menu import Menu, Option


class RepeatModeMenu(Menu):
    def _generate_options(self) -> typing.List['Option']:
        options = [
            Option(
                text='Off',
                callback=self.spotify_client.repeat,
                args=('off', )
            ),
            Option(
                text='All',
                callback=self.spotify_client.repeat,
                args=('context', )
            ),
            Option(
                text='Only',
                callback=self.spotify_client.repeat,
                args=('track', )
            )
        ]

        return options
