import typing

from sporofi.exception import UserCancel

if typing.TYPE_CHECKING:
    from sporofi.menu import Option
    from spotipy import Spotify
    from rofi import Rofi


class Menu:
    PROMPT = ''
    MESSAGE = None

    def __init__(self,
                 spotify_client: 'Spotify',
                 rofi: 'Rofi',
                 user_keys: typing.Dict[int, typing.Tuple[str, str]] = None):
        self.spotify_client = spotify_client
        self.rofi = rofi
        self._options = None

        self.user_keys = user_keys if user_keys else dict()

    def get_options(self) -> typing.List['Option']:
        if not self._options:
            self._options = self._generate_options()

        return self._options

    def show(self) -> typing.Tuple[int, int]:
        options = self.get_options()

        index, key = self.rofi.select(
            prompt=self.PROMPT,
            options=[i.text for i in options],
            message=self.MESSAGE,
            **{f'key{number}': hotkey for number, hotkey in self.user_keys.items()}
        )

        if key == -1:
            raise UserCancel

        return index, key

    def run(self):
        options = self.get_options()
        index, key_number = self.show()

        selected_options = options[index]
        key = selected_options.get_key(key_number)

        if key.is_menu():
            next_menu = key.next_menu(self.spotify_client, self.rofi, *key.args)
            next_menu.run()
        else:
            key.callback(*key.args)

    def _generate_options(self) -> typing.List['Option']:
        raise NotImplemented
