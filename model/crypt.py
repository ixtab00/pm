from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from model.model import Credentials
from datetime import datetime
from typing import Tuple
from hashlib import sha256

class Encrypt:
    def __init__(self, secret: str, timeformat: str, encoding: str = "UTF-8"):
        self._secret: str = sha256(secret.encode(encoding)).digest()
        self._timeformat: str = timeformat
        self._encoding: str = encoding

    @property
    def secret(self):
        raise ValueError("Could not access the secret.")
    
    @secret.setter
    def secret(self):
        raise ValueError("Could not change the secret.")

    def encrypt(self, pwd: str) -> Tuple:
        cipher = AES.new(self._secret, AES.MODE_CBC)
        return (cipher.encrypt(pad(pwd.encode(self._encoding), AES.block_size)), cipher.iv)

    def decrypt(self, epwd: bytes, iv: bytes) -> str:
        cipher = AES.new(self._secret, AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(epwd), AES.block_size).decode(encoding=self._encoding)

    def create_record(self, user_id: int, account: str, login: str, pwd: str) -> Credentials:
        creds = Credentials(
            login = login,
            account = account,
            password = b"",
            iv = b"",
            user_id=user_id,
            date=datetime.strftime(datetime.now(), self._timeformat)
        )
        creds.password, creds.iv = self.encrypt(pwd)
        return creds