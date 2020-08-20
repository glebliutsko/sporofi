import typing

from sporofi.menu import Menu, Option, Key


class TracksMenu(Menu):
    PROMPT = 'track'

    @property
    def _context(self) -> str or None:
        raise NotImplemented

    def _get_tracks(self) -> list:
        raise NotImplemented

    def _generate_options(self) -> typing.List['Option']:
        tracks = self._get_tracks()
        uris_list = [track['uri'] for track in tracks]
        options = []

        for track in tracks:
            options.append(Option(
                text=f'{track["artists"][0]["name"]} - {track["name"]}',
                keys={
                    Key.ENTER: Key(callback=self._start_playing, args=(uris_list, track['uri']))
                }
            ))

        return options

    def _start_playing(self, uris: typing.List[str], uri_start: str):
        if not self._context or self._context.split(':')[1] == 'artist':
            self.spotify_client.start_playback(uris=uris, offset=dict(uri=uri_start))
        else:
            self.spotify_client.start_playback(context_uri=self._context, offset=dict(uri=uri_start))
