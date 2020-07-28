import typing


class Option:
    def __init__(self,
                 text: str,
                 callback: typing.Callable,
                 args: typing.Tuple = None):
        self.text = text
        self.callback = callback
        self.args = args if args else tuple()

    def is_menu(self):
        return isinstance(self.callback, type)
