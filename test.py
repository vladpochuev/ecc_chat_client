import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

private_key1 = ec.generate_private_key(ec.SECP256R1())
public_key1 = private_key1.public_key()

private_key2 = ec.generate_private_key(ec.SECP256R1())
public_key2 = private_key2.public_key()

secret1 = private_key1.exchange(ec.ECDH(), public_key2)
secret2 = private_key2.exchange(ec.ECDH(), public_key1)

print(secret1)
print(secret2)
print(secret2 == secret1)


key1 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"handshake"
).derive(secret1)

key2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"handshake"
).derive(secret2)

print(key1)
print(key2)

aes1 = AESGCM(key1)
nonce = os.urandom(12)
cipher = aes1.encrypt(nonce, b"Test message", None)

aes2 = AESGCM(key2)
result = aes2.decrypt(nonce, cipher, None)
print(result)
