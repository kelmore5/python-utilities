import os
from dataclasses import dataclass

import datetime
import dill
import typing
from typing import Union, Any, IO, Optional

from .Utils import Utils


@dataclass
class CharCount:
    characters: int
    lines: int
    words: int

    def __init__(self, characters: int = None, lines: int = None, words: int = None):
        self.characters = characters
        self.lines = lines
        self.words = words


class Files:
    directory: str
    file_name: str

    full_path: str

    def __init__(self, file_path: str = None, file_name: str = None, full_path: str = None,
                 save_on_init: bool = False):
        if full_path is not None and file_path is None and file_name is None:
            file_path = os.path.dirname(full_path)
            file_name = os.path.basename(full_path)

        self.file_name = file_name
        self.directory = file_path if file_path != '' else None

        self._update_full_path()
        if save_on_init:
            if self.directory is not None:
                self.create_path()

            if self.has_full_path() and not os.path.isfile(self.full_path):
                with open(self.full_path, 'w') as output:
                    output.write('')

    def __copy__(self, file_path: Optional[str] = None, file_name: Optional[str] = None) -> 'Files':
        file_path: str = Utils.first_non_none(file_path, self.directory)
        file_name: str = Utils.first_non_none(file_name, self.file_name)
        return Files(file_path=file_path, file_name=file_name, save_on_init=False)

    # Files (class) related operations

    @staticmethod
    def concat(*paths: str) -> str:
        return os.path.join(*paths)

    @staticmethod
    def timestamp() -> str:
        return datetime.datetime.today().strftime('%Y-%m-%d_%H-%M')

    # Directory related operations

    @staticmethod
    def clear_directory_(directory: str) -> bool:
        if os.path.exists(directory) and not os.path.isfile(directory):
            if os.path.isfile(directory):
                return False

            files = Files.get_all_files_(directory)
            for file_name in files:
                full_path: str = Files.concat(directory, file_name)
                if os.path.exists(full_path):
                    os.remove(Files.concat(directory, file_name))
        return True

    @staticmethod
    def create_path_(path: str = None) -> Union[str, None]:
        """
        Checks for existence of a file path and if it does not exist, creates it.
            Returns the created path
        :param path: (str) The path to be checked and/or created. If path is None,
            Files will check for an internal path to use.
            If none is found, a ValueError will be raised
        :return: The confirmed path
        """
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.isfile(path):
            return None
        return path

    @staticmethod
    def get_all_files_(directory: str):
        files = []
        for directories in os.walk(directory):
            files.extend(directories[2])
            break
        return files

    @staticmethod
    def get_dir_path_(file_path: str = '', sys_arg: str = ''):
        try:
            return os.path.dirname(os.path.realpath(file_path))
        except NameError:
            return os.path.dirname(os.path.abspath(sys_arg))

    # File related operations

    @staticmethod
    def copy_file_(donor_path: str, recipient_path: str, ignore_overwrite: bool = True) -> bool:
        if not os.path.exists(donor_path) or (ignore_overwrite and os.path.exists(recipient_path)):
            return False

        donor: str = Files.read_file_(donor_path)
        recipient: IO = Files.open_(recipient_path)

        recipient.write(donor)
        recipient.close()

        return True

    @staticmethod
    def exists_(file_path: str):
        return os.path.exists(file_path)

    @staticmethod
    def open_(file_path: str, *args, read: bool = False,
              append: bool = False, **kwargs) -> Union[IO, None]:
        command = 'a+' if append else ('r' if read else 'w')
        return open(file_path, command, *args, **kwargs) if os.path.isfile(
            file_path) or not read else None

    @staticmethod
    def read_file_(file_path: str) -> Union[str, None]:
        if os.path.isfile(file_path):
            with open(file_path, 'r') as read_file:
                return read_file.read()
        else:
            return None

    @staticmethod
    def remove_(file_path: str) -> bool:
        if Files.exists_(file_path):
            os.remove(file_path)
        return True

    @staticmethod
    def stamp_file_name_(file_path: str):
        split_file: typing.Tuple[str] = os.path.splitext(file_path)
        return split_file[0] + Files.timestamp() + split_file[1]

    # Operation on files

    @staticmethod
    def create_character_count_(file_path: str) -> Union[CharCount, None]:
        if Files.exists_(file_path):
            char = 0
            lines = 0
            words = 0

            in_pipe = open(file_path, "r")
            for k in in_pipe:
                char += len(k)
                lines += 1
                k.split()
                words += len(k.split())
            return CharCount(characters=char, words=words, lines=lines)
        return None

    @staticmethod
    def get_line_number_of_word_(word: str, file_path: str) -> Union[int, None]:
        """ prec: file is a valid path, word is a string
                    postc: returns the line number of the word in the file"""
        if Files.exists_(file_path):
            in_pipe = open(file_path, "r")

            line_number: int = 0
            for k in in_pipe:
                line_number += 1
                if word in k.split():
                    return line_number
        return None

    @staticmethod
    def quarry_in_file_(quarry: str, file_path: str):
        """ prec: file is a valid path, quarry is a string
                    postc: returns True if the quarry is in the file, false otherwise"""
        return quarry in Utils.first_non_none(Files.read_file_(file_path), '')

    # Python object operations

    @staticmethod
    def save_object_(obj: Any, file_path: str) -> bool:
        """ prec: obj is any python variable and filename is a string
                    postc: saves the object to a file"""
        with open(file_path, 'wb') as output:
            dill.dump(obj, output)
        return True

    @staticmethod
    def load_object_(file_path: str) -> Union[Any, None]:
        """ prec: filename is a string
                    postc: returns the Python object saved in the file"""
        if not os.path.isfile(file_path):
            return None

        with open(file_path, 'rb') as output:
            return dill.load(output)

    # Internal operations - same as above

    def clear_directory(self) -> bool:
        return Files.clear_directory_(self._check_directory(check_exists=True))

    def create_path(self) -> str:
        return Files.create_path_(self._check_directory())

    def get_all_files(self):
        return Files.get_all_files_(self._check_directory())

    def get_dir_path(self):
        return self._check_directory()

    def copy_file(self, recipient_path: str, ignore_overwrite: bool = True):
        return Files.copy_file_(self._check_full_path(check_exists=True), recipient_path,
                                ignore_overwrite=ignore_overwrite)

    def get_file_name(self, with_stamp: bool = False):
        return Files.stamp_file_name_(self._check_file_name()) if with_stamp else self.file_name

    def get_full_path(self, with_stamp: bool = False):
        return self.stamp_file() if with_stamp else self.full_path

    def exists(self):
        return Files.exists_(self._check_full_path())

    def open(self, *args, read: bool = False, append: bool = False, **kwargs):
        return Files.open_(self._check_full_path(), read=read, append=append, *args, **kwargs)

    def overwrite(self, content: str) -> bool:
        overwriting: IO = self.open()
        overwriting.write(content)
        overwriting.close()
        return True

    def overwrite_by_file(self, donor_path: str):
        return Files.copy_file_(donor_path, self._check_full_path(), ignore_overwrite=True)

    def read_file(self):
        return Files.read_file_(self._check_full_path(check_exists=True))

    def remove(self, check_exists: bool = False) -> bool:
        return Files.remove_(self._check_full_path(check_exists=check_exists))

    def stamp_file(self):
        return Files.stamp_file_name_(self._check_full_path())

    def get_character_count(self) -> CharCount:
        return Files.create_character_count_(self._check_full_path(check_exists=True))

    def get_line_number_of_word(self, word: str) -> int:
        return Files.get_line_number_of_word_(word, self._check_full_path(check_exists=True))

    def get_number_of_lines(self) -> int:
        return Files.create_character_count_(self._check_full_path(check_exists=True)).lines

    def has_full_path(self) -> bool:
        return self.directory is not None and self.file_name is not None

    def quarry_in_file(self, quarry: str) -> bool:
        return Files.quarry_in_file_(quarry, self._check_full_path(check_exists=True))

    def save_object(self, obj: Any) -> bool:
        return Files.save_object_(obj, self._check_full_path())

    def load_object(self) -> Any:
        return Files.load_object_(self._check_full_path(check_exists=True))

    def update_file_name(self, file_name: str):
        self.file_name = file_name
        if self.directory is not None:
            self.update_full_path(Files.concat(self.directory, self.file_name))

    def update_directory(self, directory: str):
        self.directory = directory
        if self.file_name is not None:
            self.update_full_path(Files.concat(self.directory, self.file_name))

    def update_full_path(self, full_path: str):
        split_path: typing.Tuple[str] = os.path.split(full_path)
        self.directory = split_path[0]
        self.file_name = split_path[1]
        self._update_full_path()

    # Internal class functions

    def _check_full_path(self, check_exists: bool = False) -> str:
        if not self.has_full_path():
            raise ValueError('Either the file name or directory was not defined within the class')
        elif check_exists and not Files.exists_(str(self.full_path)):
            raise ValueError('The specified file path at {} does not exist'.format(self.full_path))

        self._update_full_path()
        return self.full_path

    def _check_directory(self, check_exists: bool = False) -> str:
        if self.directory is None:
            raise ValueError('No directory was defined within the class')
        elif check_exists and not Files.exists_(self.directory):
            raise ValueError('The specified directory does not exist')
        return self.directory

    def _check_file_name(self) -> str:
        if self.file_name is None:
            raise ValueError('No file name was defined within the class')
        return self.file_name

    def _update_full_path(self):
        if self.directory is None:
            self.full_path = self.file_name
        elif self.file_name is None:
            self.full_path = self.directory
        else:
            self.full_path = Files.concat(self.directory, self.file_name)
        return self.full_path
