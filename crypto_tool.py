#!/usr/bin/env python3
"""
Konsolenbasiertes Ver-/Entschlüsselungsprogramm mit Fernet (symmetrische Verschlüsselung).

Ein beliebiger Master-Key (Passwort) wird via PBKDF2-HMAC-SHA256 in einen
gültigen 32-Byte-Fernet-Schlüssel abgeleitet. Der verwendete Salt wird dem
verschlüsselten Text vorangestellt (base64-kodiert), damit beim Entschlüsseln
mit demselben Passwort wieder derselbe Schlüssel abgeleitet werden kann.

Benötigtes Paket: cryptography
    pip install cryptography
"""

import base64
import getpass
import os
import sys

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_LEN = 16          # Bytes
KDF_ITERATIONS = 480_000  # aktuell von OWASP empfohlene Mindestanzahl für PBKDF2-SHA256


def derive_key(master_key: str, salt: bytes) -> bytes:
    """Leitet aus dem Master-Key und einem Salt einen gültigen Fernet-Schlüssel ab."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    key = kdf.derive(master_key.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def encode_message(master_key: str, message: str) -> str:
    """Verschlüsselt eine Nachricht und gibt einen base64-kodierten String
    (Salt + Fernet-Token) zurück, der für die Entschlüsselung benötigt wird."""
    salt = os.urandom(SALT_LEN)
    key = derive_key(master_key, salt)
    f = Fernet(key)
    token = f.encrypt(message.encode("utf-8"))
    # Salt + Token zusammenfassen, damit beim Decode der Salt bekannt ist
    payload = salt + token
    return base64.urlsafe_b64encode(payload).decode("utf-8")


def decode_message(master_key: str, encoded_payload: str) -> str:
    """Entschlüsselt eine mit encode_message erzeugte Nachricht."""
    try:
        raw = base64.urlsafe_b64decode(encoded_payload.encode("utf-8"))
    except Exception as e:
        raise ValueError(f"Ungültiges Eingabeformat (Base64-Fehler): {e}")

    if len(raw) <= SALT_LEN:
        raise ValueError("Eingabe ist zu kurz, um gültig zu sein.")

    salt, token = raw[:SALT_LEN], raw[SALT_LEN:]
    key = derive_key(master_key, salt)
    f = Fernet(key)

    try:
        decrypted = f.decrypt(token)
    except InvalidToken:
        raise ValueError("Entschlüsselung fehlgeschlagen: falscher Master-Key oder Daten beschädigt/manipuliert.")

    return decrypted.decode("utf-8")


def prompt_master_key(confirm: bool = False) -> str:
    key = getpass.getpass("Master-Key eingeben: ")
    if not key:
        print("Master-Key darf nicht leer sein.")
        sys.exit(1)
    if confirm:
        key2 = getpass.getpass("Master-Key bestätigen: ")
        if key != key2:
            print("Die eingegebenen Master-Keys stimmen nicht überein.")
            sys.exit(1)
    return key


def menu():
    print("=" * 50)
    print(" Fernet Ver-/Entschlüsselungstool")
    print("=" * 50)
    print("1) Nachricht verschlüsseln (encode)")
    print("2) Nachricht entschlüsseln (decode)")
    print("3) Beenden")
    return input("Auswahl: ").strip()


def main():
    while True:
        choice = menu()

        if choice == "1":
            master_key = prompt_master_key(confirm=True)
            message = input("Nachricht eingeben: ")
            try:
                result = encode_message(master_key, message)
            except Exception as e:
                print(f"Fehler beim Verschlüsseln: {e}")
                continue
            print("\nVerschlüsselte Nachricht (bitte sicher aufbewahren):")
            print(result)
            print()

        elif choice == "2":
            master_key = prompt_master_key(confirm=False)
            payload = input("Verschlüsselte Nachricht eingeben: ").strip()
            try:
                result = decode_message(master_key, payload)
            except ValueError as e:
                print(f"\nFehler: {e}\n")
                continue
            except Exception as e:
                print(f"\nUnerwarteter Fehler: {e}\n")
                continue
            print("\nEntschlüsselte Nachricht:")
            print(result)
            print()

        elif choice == "3":
            print("Auf Wiedersehen.")
            break

        else:
            print("Ungültige Auswahl, bitte erneut versuchen.\n")


if __name__ == "__main__":
    main()