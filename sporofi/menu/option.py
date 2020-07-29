import typing


class Option:
    def __init__(self,
                 text: str,
                 callback: typing.Callable = None,
                 next_menu: 'type' = None,
                 args: typing.Tuple = None):
        assert callback or next_menu, 'Set only callback or next_menu'
        assert not callback or not next_menu, 'Set only callback or next_menu'

        self.text = text
        self.callback = callback
        self.next_menu = next_menu
        self.args = args if args else tuple()

    def is_menu(self):
        return self.next_menu is not None
