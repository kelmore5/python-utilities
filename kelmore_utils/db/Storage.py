import base64
import os
import pickle
import sys
from getpass import getpass

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
from typing import Optional

from ..Files import Files

MODULE_PATH: str = ''
try:
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
except NameError:
    MODULE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))


class Storage:
    salt_seed = 'A9bJbZ1UF4JAgwB90yFLTSlGoRrWjV'
    database: dict

    passphrase_file: Files
    secrets_db_file: Files
    passphrase_size: int  # 512-bit passphrase
    key_size: int  # 256-bit key
    block_size: int  # 16-bit blocks
    iv_size: int  # 128-bits to initialise
    sal_size: int  # 64-bits of salt

    pass_phrase: str

    def __init__(self, main_module_path: str, pass_phrase_file: Optional[Files] = None,
                 secrets_db_file: Optional[Files] = None):
        pass_phrase_file = Storage.get_default_pass_phrase(main_module_path) \
            if pass_phrase_file is None else pass_phrase_file
        secrets_db_file = Storage.get_default_secrets(main_module_path) \
            if secrets_db_file is None else secrets_db_file

        self.passphrase_file = pass_phrase_file
        self.secrets_db_file = secrets_db_file
        self.passphrase_size = 64  # 512-bit passphrase
        self.key_size = 32  # 256-bit key
        self.block_size = 16  # 16-bit blocks
        self.iv_size = 16  # 128-bits to initialise
        self.sal_size = 8  # 64-bits of salt

        self.set_pass_phrase()
        self.set_database()

    def get_salt(self, key):
        # Salt is generated as the hash of the key with it's own salt acting like a seed value
        return PBKDF2(key, Storage.salt_seed).read(self.sal_size)

    def encrypt(self, plaintext, salt):
        # Pad plaintext, then encrypt it with a new, randomly initialised cipher.
        # Will not preserve trailing whitespace in plaintext!

        # Initialise Cipher Randomly
        init_vector = os.urandom(self.iv_size)

        # Prepare cipher key:
        pass_key = PBKDF2(self.pass_phrase, salt).read(self.key_size)

        cipher = AES.new(pass_key, AES.MODE_CBC, init_vector)  # Create cipher

        # Pad and encrypt
        crypt: str = plaintext + ' ' * (self.block_size - (len(plaintext) % self.block_size))
        return init_vector + cipher.encrypt(str.encode(crypt))

    def decrypt(self, cipher_text, salt):
        # Reconstruct the cipher object and decrypt. Will not preserve trailing whitespace in
        # the retrieved value

        # Prepare cipher key:
        key = PBKDF2(self.pass_phrase, salt).read(self.key_size)

        # Extract IV:
        init_vector = cipher_text[:self.iv_size]
        cipher_text = cipher_text[self.iv_size:]

        # Reconstruct cipher (IV isn't needed for edecryption so is set to zeros)
        cipher = AES.new(key, AES.MODE_CBC, init_vector)

        # Decrypt and depad
        return cipher.decrypt(cipher_text).rstrip(str.encode(' '))

    def store(self, key, value):
        # Sore key-value pair safely and save to disk
        self.database[key] = self.encrypt(value, self.get_salt(key))
        with open(self.secrets_db_file.full_path, 'wb') as file:
            pickle.dump(self.database, file)

    def retrieve(self, key):
        # Fetch key-value pair
        return self.decrypt(self.database[key], self.get_salt(key)).decode()

    def check_key(self, key: str):
        return key in self.database

    def require(self, key):
        # Test if key is stored, if not, prompt the user for it while hiding their input
        # from shoulder-surfers
        if not self.check_key(key):
            self.store(key, getpass('Please enter a value for "%s":' % key))

    def clear_db(self):
        self.passphrase_file.remove()
        self.secrets_db_file.remove()

        self.set_pass_phrase()
        self.set_database()

    def set_pass_phrase(self):
        self.pass_phrase = self.get_pass_phrase()

    def get_pass_phrase(self) -> str:
        pass_phrase_file = self.passphrase_file.full_path

        # Acquire passphrase:
        try:
            with open(pass_phrase_file, 'r') as file:
                pass_phrase = file.read()
            if not pass_phrase:
                raise IOError
        except IOError:
            self.passphrase_file.remove()
            self.secrets_db_file.remove()

            with open(pass_phrase_file, 'wb') as file:
                # Random passphrase
                pass_phrase = os.urandom(self.passphrase_size)
                file.write(base64.b64encode(pass_phrase))
        else:
            # Decode if loaded from already extant file
            pass_phrase = base64.b64decode(pass_phrase)

        return pass_phrase

    def set_database(self):
        self.database = self.get_database()

    def get_database(self) -> dict:
        secrets_file: str = self.secrets_db_file.full_path
        try:
            with open(secrets_file, 'rb') as file:
                database: dict = pickle.load(file)
            if database == {}:
                raise IOError
        except (IOError, EOFError):
            database = {}
            with open(secrets_file, 'wb') as file:
                pickle.dump(database, file)
        return database

    @staticmethod
    def example():
        file_path: str = os.path.dirname(__file__)
        pass_phrase: Files = Files(file_path=file_path, file_name='secrets.p')
        secrets: Files = Files(file_path=file_path, file_name='secrets')

        storage = Storage(main_module_path=MODULE_PATH, pass_phrase_file=pass_phrase,
                          secrets_db_file=secrets)
        storage.require('id')
        storage.require('password1')
        print('')
        print('Stored Data:')
        for key in storage.database:
            print(key, storage.retrieve(key))

    @staticmethod
    def get_default_pass_phrase(main_module_path: str) -> Files:
        return Files(file_path=Files.concat(main_module_path, 'database', 'keys'),
                     file_name='secret.p')

    @staticmethod
    def get_default_secrets(main_module_path: str) -> Files:
        return Files(file_path=Files.concat(main_module_path, 'database', 'keys'),
                     file_name='secrets')
