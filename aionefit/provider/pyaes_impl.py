from pyaes import AESModeOfOperationECB, Encrypter, Decrypter, PADDING_NONE
import hashlib
import base64
import logging

_LOGGER = logging.getLogger(__name__)


class AESCipher(object):
    """Helperclass to handle the en/decryption of the messages
    """
    def __init__(self, magic, access_key, password):
        self.bs = 16
        self.key = hashlib.md5(bytearray(access_key, "utf8") + magic).digest()
        self.key += hashlib.md5(magic + bytearray(password, "utf8")).digest()

    def encrypt(self, raw):
        if len(raw) % self.bs != 0:
            raw = self._pad(raw)
        cipher = Encrypter(AESModeOfOperationECB(self.key),
                           padding=PADDING_NONE)
        ciphertext = cipher.feed(raw) + cipher.feed()

        return base64.b64encode(ciphertext)

    def decrypt(self, enc):
        # trying to decrypt empty data fails
        if not enc:
            return ""
        enc = base64.b64decode(enc)
        cipher = Decrypter(AESModeOfOperationECB(self.key),
                           padding=PADDING_NONE)
        decrypted = cipher.feed(enc) + cipher.feed()
        try:
            r = decrypted.decode("utf8").rstrip(chr(0))
        except UnicodeDecodeError as e:
            raise SystemError("Decryption error (%s). Wrong password?", e)
        return r

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(0)
