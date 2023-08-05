""" Entrypoint for f-encrypt commands """
import os
import sys
from getpass import getpass
from pathlib import Path

import click

import fencrypt.aes as aes


KEY_PROMPT = "Enter Key: "


def is_replace_mode():
    """ Check if "F_ENCRYPT_REPLACE" is "true" - if it is, replace the file instead of printing """
    env_var = "F_ENCRYPT_REPLACE"
    return env_var in os.environ and os.environ[env_var].lower() == "true"


def assert_path_exists(path):
    """ Ensure that a given path exists """
    if not Path(path).exists():
        sys.stderr.write(f"ERROR - file not found: {path}\n")
        sys.exit(1)
    if not Path(path).is_file():
        sys.stderr.write(f"ERROR - {path} must be a file\n")
        sys.exit(1)


@click.option("--key", "-k", envvar="F_ENCRYPT_KEY", default=None, help="Secret Key")
@click.argument("path")
@click.command()
def encrypt(path, key):
    """ Encrypt the given file """
    assert_path_exists(path)
    key = key if key else getpass(prompt=KEY_PROMPT)
    with open(path, "r") as fil:
        plaintext = fil.read()
    ciphertext = aes.encrypt(key, plaintext)
    if is_replace_mode():
        with open(path, "w") as fil:
            fil.write(ciphertext)
    else:
        print(ciphertext)


@click.option("--key", "-k", envvar="F_ENCRYPT_KEY", default=None, help="Secret Key")
@click.argument("path")
@click.command()
def decrypt(path, key):
    """ Dycrypt a given file """
    assert_path_exists(path)
    key = key if key else getpass(prompt=KEY_PROMPT)
    with open(path, "r") as fil:
        ciphertext = fil.read()
    plaintext = aes.decrypt(key, ciphertext)
    if is_replace_mode():
        with open(path, "w") as fil:
            fil.write(plaintext)
    else:
        print(plaintext)
