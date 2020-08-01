import typing

from sporofi.menu import Menu, Option, Key


class TracksMenu(Menu):
    PROMPT = 'track'

    @property
    def _context(self) -> str or None:
        raise NotImplemented

    def _get_tracks(self) -> dict:
        raise NotImplemented

    def _generate_options(self) -> typing.List['Option']:
        tracks = self._get_tracks()

        options = []
        uris_list = list(tracks.keys())
        for uri, name in tracks.items():
            options.append(Option(
                text=name,
                keys={
                    Key.ENTER: Key(callback=self._start_playing, args=(uris_list, uri))
                }
            ))

        return options

    def _start_playing(self, uris: typing.List[str], uri_start: str):
        if not self._context or self._context.split(':')[1] == 'artist':
            self.spotify_client.start_playback(uris=uris, offset=dict(uri=uri_start))
        else:
            self.spotify_client.start_playback(context_uri=self._context, offset=dict(uri=uri_start))
