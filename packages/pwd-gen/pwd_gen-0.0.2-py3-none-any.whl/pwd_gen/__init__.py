import random
import string
import crypt
import time
from Crypto.Cipher import XOR
import base64

punct = list(string.punctuation)
sp = ""
for ch in punct:
    if ch != '"':
        sp += ch


def generate(length: int):  # random password
    settings = string.ascii_letters + string.digits + sp
    result = str().join((random.choice(settings) for _ in range(0, length)))
    return result


def encrypt(passw):  # encrypt a string
    cipher = XOR.new(passw)
    return str(base64.b64encode(
        cipher.encrypt(crypt.crypt(passw, 'O248FHjbkfnjbgfnjbnsbvnj/fadknlnkgldsngsdnkdfhkjgnkbfnkd'))))[
           2:-1] + crypt.crypt(passw, passw)


def inpm():
    global lnp
    global pasw
    lnp = input('select the length of the password (type "n" to select a password): ')
    pasw = input('select a password: ') if lnp.lower() == 'n' else False


def tst():
    if pasw == False:
        p = generate(int(lnp))
        pe = encrypt(p)
        print(f'\nnormal: {p}\nencrypted: {pe}')
    else:
        pe = encrypt(pasw)
        print(f'\nnormal: {pasw}\nencrypted: {pe}')


def pause():
    while True:
        time.sleep(1)
        pause()
