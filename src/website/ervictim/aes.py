from Crypto.Cipher import AES
from Crypto.Util import randpool
from Crypto.Random import get_random_bytes
import base64

block_size = 16
key_size = 32
mode = AES.MODE_CBC

def encrypt_aes(string):
    key_bytes = get_random_bytes(key_size)
    pad = block_size - len(string.encode('utf-8')) % block_size
    data = string.encode('utf-8') + pad * chr(pad)
    iv_bytes = get_random_bytes(block_size)
    encrypted_bytes = iv_bytes + AES.new(key_bytes, mode, iv_bytes).encrypt(data)
    string_encrypted = base64.urlsafe_b64encode(str(encrypted_bytes))
    key = base64.urlsafe_b64encode(str(key_bytes))
    return (string_encrypted, key)

def decrypt_aes(key_string, encrypted_string):
    key_bytes = base64.urlsafe_b64decode(str(key_string))    
    encrypted_bytes = base64.urlsafe_b64decode(str(encrypted_string))    
    iv_bytes = encrypted_bytes[:block_size]    
    encrypted_bytes = encrypted_bytes[block_size:]
    plain_text = AES.new(key_bytes, mode, iv_bytes).decrypt(encrypted_bytes)
    pad = ord(plain_text[-1])
    plain_text = plain_text[:-pad]
    return plain_text.decode('utf-8')
