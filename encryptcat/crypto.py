from Crypto.Cipher import AES
from Crypto.Util import Padding
import os
import click


class CryptoCore(object):
    def __init__(self, key=None):
        self.key = key
        self.mode = AES.MODE_CBC

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        binary_value = value.encode()
        self._key = Padding.pad(binary_value, 16)

    def encrypt(self, message):
        try:
            if isinstance(message, str):
                message = message.encode()
            message = Padding.pad(message, 16)
        except Exception:
            raise TypeError('message type error')
        cipher = AES.new(self.key, self.mode, self.key)
        cipher_text = cipher.encrypt(message)
        return cipher_text

    def decrypt(self, message):
        cipher = AES.new(self.key, self.mode, self.key)
        plain_text = cipher.decrypt(message)
        try:
            return Padding.unpad(plain_text, 16)
        except ValueError:
            return plain_text


def encrypt_file(key: str, path: str):
    file_name = os.path.basename(path)
    dir_path = os.path.dirname(path)
    output_path = os.path.join(dir_path, file_name+'.se')
    crypt_core = CryptoCore(key)
    data = None
    with open(path, 'rb') as f:
        data = crypt_core.encrypt(f.read())

    with open(output_path, 'wb') as f:
        f.write(data)
    return output_path


def decrypt_file(key: str, path: str):
    file_name = os.path.basename(path)
    dir_path = os.path.dirname(path)
    output_path = os.path.join(dir_path, file_name[:file_name.index('.se')])
    if os.path.isfile(output_path):
        file_name = 'copy ' + file_name
        output_path = os.path.join(dir_path, file_name[:file_name.index('.se')])
    crypt_core = CryptoCore(key)
    data = None
    try:
        with open(path, 'rb') as f:
            data = crypt_core.decrypt(f.read())

        with open(output_path, 'wb') as f:
            f.write(data)
        return output_path
    except Exception as e:
        raise e


if __name__ == '__main__':

    @click.command()
    @click.argument('key')
    @click.argument('path')
    @click.option('-m', '--mode', 'mode', default='enc')
    def cli(key, path, mode):
        if mode == 'dec':
            decrypt_file(key, path)
        else:
            encrypt_file(key, path)

    cli()
