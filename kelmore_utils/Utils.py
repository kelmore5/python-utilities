import sys
from urllib import parse

import re
from typing import Any, List


class Utils:

    @staticmethod
    def first_non_none(*items: Any) -> Any:
        for item in items:
            if item is not None:
                return item
        return None

    @staticmethod
    def untested(*items: Any):
        print('\n' * 3)
        print('UNTESTED: Check object output')
        for item in items:
            print(str(item))
        print('\n' * 3)

    @staticmethod
    def print(*items: Any) -> None:
        print('\n' * 3)
        for item in items:
            print(str(item))
        print('\n' * 3)

    @staticmethod
    def is_windows() -> bool:
        return not (sys.platform == 'linux' or sys.platform == 'darwin')

    # TODO: Move below methods to Utils util class in future
    @staticmethod
    def add_http_link(url: str) -> str:
        if not re.match(r'http(s?):', url):
            url = 'http://' + url
        return url

    @staticmethod
    def get_base_site(url: str, with_suffix=True) -> str:
        url: str = Utils.normalize_link(url, with_prefix=False, only_valid=True, with_suffix=False)

        split_url = parse.urlsplit(url)
        url = split_url.netloc
        if not with_suffix:
            url_split: List[str] = url.split('.')
            return url_split[1] if url_split[0] == 'www' else url_split[0]
        return url

    @staticmethod
    def normalize_link(url: str, with_prefix: bool = True, only_valid: bool = True,
                       with_suffix=True) -> str:
        if url is None:
            return ''

        url = Utils.add_http_link(url)

        parsed = parse.urlsplit(url)
        host: str = parsed.netloc

        if with_prefix:
            host = Utils.add_http_link(host)
        else:
            if host.startswith('www.'):
                host = host[4:]

            host = Utils.add_http_link(host) if only_valid else host

        if with_suffix:
            host += parsed.path

            if parsed.query != '':
                host += '?' + parsed.query

        return host
