import typing


def get_all_page(func: typing.Callable, limit=50, *args, **kwargs):
    offset = 0
    while True:
        page = func(*args, **kwargs, offset=offset, limit=limit)

        if len(page['items']) != 0:
            yield page['items']

        offset += limit
        if page['total'] <= offset:
            return
