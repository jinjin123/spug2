import rsa
import os


def enkey():
    with open(os.path.abspath("libs/key")+'/public.pem', 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    return pubkey

def unkey():
    with open(os.path.abspath("libs/key")+'/private.pem', 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
    return privkey


def encryptPwd(text):
    pubkey = enkey()
    crypto = rsa.encrypt(text.encode(), pubkey)
    return crypto

def decryptPwd(text):
    privkey = unkey()
    pwd = rsa.decrypt(text, privkey).decode()
    return pwd
