import typing

from sporofi.exception import UserCancel

if typing.TYPE_CHECKING:
    from sporofi.menu import Option
    from spotipy import Spotify
    from rofi import Rofi


class Menu:
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi'):
        self.spotify_client = spotify_client
        self.rofi = rofi
        self._options = None

    def get_options(self):
        if not self._options:
            self._options = self._generate_options()

        return self._options

    def show(self) -> int:
        options = self.get_options()

        options_text = [i.text for i in options]
        index, key = self.rofi.select('', options_text)

        if key == -1:
            raise UserCancel

        return index

    def run(self):
        options = self.get_options()
        index = self.show()

        selected_options = options[index]
        if selected_options.is_menu():
            next_menu = selected_options.next_menu(self.spotify_client, self.rofi, *selected_options.args)
            next_menu.run()
        else:
            selected_options.callback(*selected_options.args)

    def _generate_options(self) -> typing.List['Option']:
        raise NotImplemented
