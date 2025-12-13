import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from src.python.model.encrypted_text import EncryptedText

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode("utf-8")


def get_encrypted_text(text: str, user_public_key: str) -> EncryptedText:
    user_public_key = serialization.load_pem_public_key(
        user_public_key.encode("utf-8")
    )
    secret = private_key.exchange(ec.ECDH(), user_public_key)

    key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake"
    ).derive(secret)

    aes1 = AESGCM(key)
    nonce = os.urandom(12)
    cipher_text = aes1.encrypt(nonce, text.encode(), None)
    cipher_b64 = base64.b64encode(cipher_text).decode("utf-8")
    nonce_b64 = base64.b64encode(nonce).decode("utf-8")

    return EncryptedText(cipher_b64, nonce_b64)
