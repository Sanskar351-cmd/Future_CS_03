from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os, hashlib, binascii
from flask import current_app

def get_master_key():
    cfg = current_app.config
    passphrase = cfg.get('MASTER_PASSPHRASE')
    if not passphrase:
        raise RuntimeError('MASTER_PASSPHRASE not set')
    salt_path = cfg.get('SALT_PATH')
    if os.path.exists(salt_path):
        with open(salt_path, 'rb') as f:
            salt = f.read()
    else:
        salt = get_random_bytes(16)
        with open(salt_path, 'wb') as f:
            f.write(salt)
    key = PBKDF2(passphrase.encode('utf-8'), salt, dkLen=32, count=cfg.get('KDF_ITERATIONS'))
    return key

def encrypt_file_bytes(plaintext: bytes):
    file_key = get_random_bytes(32)
    nonce = get_random_bytes(12)
    cipher = AES.new(file_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    master_key = get_master_key()
    wrap_nonce = get_random_bytes(12)
    wrap_cipher = AES.new(master_key, AES.MODE_GCM, nonce=wrap_nonce)
    filekey_enc, wrap_tag = wrap_cipher.encrypt_and_digest(file_key)
    return ciphertext, nonce, tag, binascii.hexlify(filekey_enc).decode(), binascii.hexlify(wrap_nonce).decode(), binascii.hexlify(wrap_tag).decode()

def decrypt_file_bytes(ciphertext: bytes, nonce: bytes, tag: bytes, filekey_enc_hex: str, wrap_nonce_hex: str, wrap_tag_hex: str):
    master_key = get_master_key()
    filekey_enc = binascii.unhexlify(filekey_enc_hex)
    wrap_nonce = binascii.unhexlify(wrap_nonce_hex)
    wrap_tag = binascii.unhexlify(wrap_tag_hex)
    wrap_cipher = AES.new(master_key, AES.MODE_GCM, nonce=wrap_nonce)
    file_key = wrap_cipher.decrypt_and_verify(filekey_enc, wrap_tag)
    cipher = AES.new(file_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
