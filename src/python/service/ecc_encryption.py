import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from src.python.model import EncryptedText

private_key_path = os.path.join(os.getenv("PRIVATE_KEY_DIR"), "private_key.pem")

if os.path.exists(private_key_path):
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=os.getenv("KEY_PASSWORD").encode("utf-8")
        )
else:
    private_key = ec.generate_private_key(ec.SECP256R1())
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(os.getenv("KEY_PASSWORD").encode("utf-8"))
    )

    with open(private_key_path, "wb") as f:
        f.write(pem)

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


def get_decrypted_text(encrypted_text: EncryptedText, user_public_key: str) -> str:
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

    cipher = base64.b64decode(encrypted_text.cipher_text)
    nonce = base64.b64decode(encrypted_text.nonce)

    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce, cipher, None)

    return plaintext.decode("utf-8")
