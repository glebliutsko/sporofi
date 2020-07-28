import typing

from sporofi.menu import Menu, Option


class PlaylistsMenu(Menu):
    def _generate_options(self) -> typing.List[Option]:
        playlists = self.spotify_client.current_user_playlists()

        options = [Option(
            text='Liked songs',
            callback=self._play_liked,
            args=()
        )]

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
