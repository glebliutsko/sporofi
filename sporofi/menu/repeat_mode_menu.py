import typing

from sporofi.menu import Menu, Option, Key


class RepeatModeMenu(Menu):
    PROMPT = 'mode'

    def _generate_options(self) -> typing.List['Option']:
        options = [
            Option(
                text='Off',
                keys={Key.ENTER: Key(callback=self.spotify_client.repeat, args=('off', ))}
            ),
            Option(
                text='All',
                keys={Key.ENTER: Key(callback=self.spotify_client.repeat, args=('context', ))}
            ),
            Option(
                text='Only',
                keys={Key.ENTER: Key(callback=self.spotify_client.repeat, args=('track', ))}
            )
        ]

        return options
