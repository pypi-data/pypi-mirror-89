""" AES cipher methods """
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


def _pad(raw):
    """ AES uses blocks of 16 chars at a time. Pad the block out with extra chars if needed """
    # AES block size is 16
    block_size = AES.block_size
    # use a different padding char depending on the strings length mod 16
    pad_chr = chr(block_size - len(raw) % block_size)
    # pad_length is the # of chars to add to bring the raw str to a multiple of 16 chars
    pad_length = (block_size - len(raw)) % 16
    padding = pad_length * pad_chr
    return raw + padding


def _unpad(padded):
    """ Remove the padding applied by _pad() """
    return padded[: -ord(padded[len(padded) - 1 :])]


def encrypt(secret_key, plaintext):
    """ Encrypt given plaintext and return as base64 string """
    key = hashlib.sha256(secret_key.encode()).digest()
    padded_pt = _pad(plaintext)
    init_vector = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    encoded_pt = padded_pt.encode()
    ciphertext = cipher.encrypt(encoded_pt)
    ct_b64 = base64.b64encode(init_vector + ciphertext)
    return ct_b64.decode("UTF-8")


def decrypt(secret_key, ct_b64):
    """ Decrypt given base64 ciphertext and return plaintext string """
    ct_decoded = base64.b64decode(ct_b64)
    init_vector = ct_decoded[: AES.block_size]
    key = hashlib.sha256(secret_key.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    encoded_padded_pt = cipher.decrypt(ct_decoded[AES.block_size :])
    padded_pt = encoded_padded_pt.decode("utf-8")
    plaintext = _unpad(padded_pt)
    return str(plaintext)
