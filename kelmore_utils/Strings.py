import re
from typing import Optional, Iterable, List


class StringTools:

    @staticmethod
    def join(item_list: List[str], param: Optional[str] = '\n'):
        return param.join(item_list)

    @staticmethod
    def replace_non_ascii(string: str, replacement: str = ' ', with_space: bool = True):
        regex: str = '[^0-9a-zA-Z{}]+'.format(' ' if with_space else '')
        return re.sub(re.compile(regex, re.I), replacement, string)

    @staticmethod
    def replace_whitespace(string: str, replacement: Optional[str] = ' '):
        return re.sub(r'\s+', replacement, string).strip()

    @staticmethod
    def strip_or_none(string: str):
        return string.strip() if string is not None else None

    @staticmethod
    def convert_null(string: str):
        return '' if string is None else string.strip()

    @staticmethod
    def only_ascii(string: str):
        return ''.join([i if ord(i) < 128 else ' ' for i in string])

    @staticmethod
    # Mostly used for database stuff
    def normalize_string(string: str) -> str:
        return StringTools.only_alpha(string.replace(' ', '_')).lower()

    @staticmethod
    # Mostly used for database stuff
    def regularize_string(string: str) -> str:
        return string.replace('_', ' ').title().replace('Url', 'URL')

    @staticmethod
    def string_ends_with_array(check_string: str, ends_with_checks: Iterable[str]):
        for string in ends_with_checks:
            if check_string.lower().strip().endswith(string.lower()):
                return True
        return False

    @staticmethod
    def array_in_string(check_string: str, compare_strings: Iterable[str]):
        for string in compare_strings:
            if string in check_string:
                return True
        return False

    @staticmethod
    def remove_whitespace(string: str) -> str:
        return ''.join(string.split())

    @staticmethod
    def count_substring(string: str, search: str):
        return string.count(search)

    @staticmethod
    def only_alpha(string: str, plus_space: Optional[bool] = False) -> str:
        reg: str = None
        if plus_space:
            reg = r'([^\s\w]|_)+'
        else:
            reg = r'\W+'
        return re.sub(reg, '', string)

    @staticmethod
    def is_ascii(string):
        """ prec: s is a string
            postc: returns true if all characters in the string are ascii values,
                false otherwise"""
        return all(ord(c) < 128 for c in string)

    @staticmethod
    def last_char(string):
        """ prec: x is a string
            postc: returns the last character of the string."""
        return string[-1]  # method stub or function stub

    @staticmethod
    def last_non_whitespace_char(string):
        """ prec: x is a string
            postc: returns the last non-whitespace character"""
        string = string.rstrip()
        return string[-1]  # method stub or function stub

    @staticmethod
    def biggest_word_length(text):
        """ precondition:  text is a string
            postcondition: returns the length of the longest word in x
                (do not worry about punctuation)"""
        return len(max(text.split(), key=len))

    @staticmethod
    def biggest_word(text):
        """ precondition:  text is a string
            postcondition: returns the the longest word in x (do not worry about punctuation)"""
        return max(text.split(), key=len)

    @staticmethod
    def half_of_alphabet(string):
        """ prec:  x is an alpha string
            postc:  returns "in the first half" if x is in the first half of the
                    alphabet; otherwise "in the second half" """
        # whole expression is one of two terms - first half or second half
        # depending on string x
        return "in the first half" if string.lower() < "m" else "in the second half"

    @staticmethod
    def triangle(char, size):
        if size == 0:
            return
        StringTools.triangle(char, size - 1)
        print(char * size)

    @staticmethod
    def triangle_backwards(char, size):
        if size == 0:
            return
        print(char * size)
        StringTools.triangle_backwards(char, size - 1)

    @staticmethod
    def vowel_mole(string):
        """ prec: x is a string
            postc: returns a string with all all vowels (except y) in order in
                    the string.  Case must be preserved."""
        vowels: List[str] = ['a', 'e', 'i', 'o', 'u']
        string = [char for char in string if char in vowels]
        return "".join(string)

    @staticmethod
    def f2c(temp_f):
        """ precondition:   tempF is a number
            postcondition:  returns tempF converted to centigrade"""
        return 5.0 / 9.0 * (temp_f - 32)

    @staticmethod
    def c2f(temp_c):
        """ precondition:   tempC is a number
            postcondition:  returns tempC converted to farenheit"""
        return (9.0 * temp_c) / 5.0 + 32
