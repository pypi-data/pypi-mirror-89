import base64
import argparse


from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


DEFAULT_AES_KEY = 'Emotibot20201204'
DEFAULT_IV = 'Emotibot20201204'
mode = AES.MODE_CBC

BLOCK_SIZE = 16
KEY_SIZE = 16


def process_key(key):
    if len(key) >= KEY_SIZE:
        return key[:KEY_SIZE]
    key += '0' * (KEY_SIZE - len(key))
    return key


def encrypt(text, aes_key=DEFAULT_AES_KEY, iv=DEFAULT_IV):
    cryptor = AES.new(process_key(aes_key).encode('utf8'), mode, process_key(iv).encode('utf8'))
    padded = pad(bytes(text, encoding='utf8'), BLOCK_SIZE)
    result = cryptor.encrypt(padded)
    return base64.b64encode(result).decode()


def decrypt(text, aes_key=DEFAULT_AES_KEY, iv=DEFAULT_IV):
    cryptor = AES.new(process_key(aes_key).encode('utf8'), mode, process_key(iv).encode('utf8'))
    decode = base64.b64decode(text)
    result = cryptor.decrypt(decode)
    return unpad(result, BLOCK_SIZE).decode('utf8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AES128/CBC/PKCS5Padding Encrypt')
    parser.add_argument('text', type=str)
    parser.add_argument('--aes_key', type=str, default=DEFAULT_AES_KEY)
    parser.add_argument('--iv', type=str, default=DEFAULT_IV)
    parser.add_argument('--mode', type=int, default=0, help="0加密;1解密")

    args = parser.parse_args()
    if args.mode == 0:
        '''加密'''
        encoded = encrypt(args.text, args.aes_key, args.iv)
        print(encoded)
    elif args.mode == 1:
        '''解密'''
        decoded = decrypt(args.text, args.aes_key, args.iv)
        print(decoded)


