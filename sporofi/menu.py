from enum import Enum
import typing
if typing.TYPE_CHECKING:
    from spotipy import Spotify
    from rofi import Rofi


class TypeAction(Enum):
    CALLBACK = 1
    NEXT_MENU = 2


class UserCancel(Exception):
    pass


class Option:
    def __init__(self,
                 text: str,
                 callback: typing.Callable,
                 args: typing.Tuple):
        self.text = text
        self.callback = callback
        self.args = args

    def is_menu(self):
        return isinstance(self.callback, type)


class Menu:
    def __init__(self, spotify_client: 'Spotify', rofi: 'Rofi',  *args):
        self.spotify_client = spotify_client
        self.rofi = rofi
        self._options = None

        self.data_last_menu = args

    def get_options(self):
        if not self._options:
            self._options = self._generate_options()

        return self._options

    def show(self) -> int:
        options = self.get_options()

        options_text = [i.text for i in options]
        index, key = self.rofi.select('Playlist', options_text, message='Select playlists')

        if key == -1:
            raise UserCancel

        return index

    def run(self):
        options = self.get_options()
        index = self.show()

        selected_options = options[index]
        if selected_options.is_menu():
            next_menu = selected_options.callback(self.spotify_client, self.rofi, *selected_options.args)
            next_menu.run()
        else:
            selected_options.callback(*selected_options.args)

    def _generate_options(self) -> typing.List[Option]:
        raise NotImplemented


class Control(Menu):
    def _generate_options(self) -> typing.List[Option]:
        options = [
            Option(
                text='Next',
                callback=self._next,
                args=()
            ),
            Option(
                text='PlayPause',
                callback=self._playpause,
                args=()
            ),
            Option(
                text='Previous',
                callback=self._previous,
                args=()
            )
        ]

        playback = self.spotify_client.current_playback()

        options.append(Option(
            text=f'Shuffle [{"on" if playback["shuffle_state"] else "off"}]',
            callback=self._shuffle,
            args=(playback["shuffle_state"], )
        ))

        if playback['repeat_state'] == 'off':
            repeat_state = 'off'
        elif playback['repeat_state'] == 'context':
            repeat_state = 'all'
        else:
            repeat_state = 'only'

        options.append(Option(
            text=f'Repeat [{repeat_state}]',
            callback=self._repeat,
            args=(playback['repeat_state'], )
        ))

        self.spotify_client.current_playback()

        return options

    def _shuffle(self, state: bool):
        self.spotify_client.shuffle(not state)

    def _repeat(self, state: str):
        def next_state(current_state: str):
            list_state = ['off', 'context', 'track']
            index = list_state.index(current_state) + 1
            if index >= len(list_state):
                index = 0

            return list_state[index]

        self.spotify_client.repeat(next_state(state))

    def _next(self):
        self.spotify_client.next_track()

    def _playpause(self):
        playback = self.spotify_client.current_playback()
        if playback['is_playing']:
            self.spotify_client.pause_playback()
        else:
            self.spotify_client.start_playback()

    def _previous(self):
        self.spotify_client.previous_track()


class Playlists(Menu):
    def _generate_options(self) -> typing.List[Option]:
        playlists = self.spotify_client.current_user_playlists()

        options = []

        options.append(Option(
            text='Liked songs',
            callback=self._play_liked,
            args=()
        ))

        for playlist in playlists['items']:
            options.append(Option(
                text=playlist['name'],
                callback=self._play_playlist,
                args=(playlist['uri'], )
            ))

        return options

    def _play_liked(self):
        def uris_liked_tracks():
            offset = 0
            while True:
                tracks = self.spotify_client.current_user_saved_tracks(50, offset)
                if len(tracks['items']) == 0:
                    return

                for track in tracks['items']:
                    yield track['track']['uri']

                offset += 50

        self.spotify_client.start_playback(uris=[uris for uris in uris_liked_tracks()])

    def _play_playlist(self, id_: str):
        self.spotify_client.start_playback(context_uri=id_)
