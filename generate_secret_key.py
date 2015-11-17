# Creates a secret key to be used with security modules

from random_password_generator import PasswordGenerator
import os

gen = PasswordGenerator()

def load_secret_key():
    with open("secret.txt") as file_handler:
        return file_handler.read().split("\n")[0]

def make_secret_key():
    """make_secret_key(void) -> returns (str)
    Returns a secret
    """
    if not os.path.exists(os.path.join(os.getcwd(), "secret.txt")):
        SECRET = gen.gen_passwd(19)[0]
        file_handler = open("secret.txt", "w")
        file_handler.write(SECRET)
        



