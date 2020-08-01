import typing

from sporofi.menu import Menu, Option, Key, RepeatModeMenu


class ControlMenu(Menu):
    def _generate_options(self) -> typing.List[Option]:
        options = [
            Option(
                text='Next',
                keys={Key.ENTER: Key(callback=self._next)}
            ),
            Option(
                text='PlayPause',
                keys={Key.ENTER: Key(callback=self._playpause)}
            ),
            Option(
                text='Previous',
                keys={Key.ENTER: Key(callback=self._previous)}
            )
        ]

        playback = self.spotify_client.current_playback()

        options.append(Option(
            text=f'Shuffle [{"on" if playback["shuffle_state"] else "off"}]',
            keys={Key.ENTER: Key(callback=self._shuffle, args=(playback["shuffle_state"], ))}
        ))

        if playback['repeat_state'] == 'off':
            repeat_state = 'off'
        elif playback['repeat_state'] == 'context':
            repeat_state = 'all'
        else:
            repeat_state = 'only'

        options.append(Option(
            text=f'Repeat [{repeat_state}]',
            keys={Key.ENTER: Key(next_menu=RepeatModeMenu)}
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
