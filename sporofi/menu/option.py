import typing


class Key:
    ENTER = 0
    USER_KEY_1 = 1
    USER_KEY_2 = 2
    USER_KEY_3 = 3
    USER_KEY_4 = 4
    USER_KEY_5 = 5
    USER_KEY_6 = 6
    USER_KEY_7 = 7
    USER_KEY_8 = 8
    USER_KEY_9 = 9

    def __init__(self, callback: typing.Callable = None, next_menu: type = None, args: tuple = None):
        assert callback or next_menu, 'Set only callback or next_menu'
        assert not callback or not next_menu, 'Set only callback or next_menu'

        self.callback = callback
        self.next_menu = next_menu
        self.args = args if args else tuple()

    def is_menu(self):
        return self.next_menu is not None


class Option:
    def __init__(self,
                 text: str,
                 keys: typing.Dict[int, Key]):
        self.text = text
        self.keys = keys

    def add_key(self, number: int, key: Key):
        self.keys[number] = key

    def get_key(self, number: int) -> Key:
        return self.keys[number]
