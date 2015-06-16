import bcrypt
import hashlib
import random
import string

NO_PASSWORD_VALUE = '*'
MIN_PASSWORD_LENGTH = 6


def encrypt_password(raw_password):
    """Salted hash password with bcrypt."""
    return bcrypt.hashpw(raw_password, bcrypt.gensalt())

def check_password(raw_password, encrypted_password):
    """Return true if password matches.
    We support new bcrypt and old sha1.
    """
    if not encrypted_password:
        return False

    try:
        hashpw = bcrypt.hashpw(raw_password, encrypted_password)
    except UnicodeEncodeError:
        return False
    return hashpw == encrypted_password


def generate_random_password(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class ComplexityError():
    # Add more error codes when we add more complexity rules
    NoErr = 0
    MinLengthErr = -1


def check_complexity(password):
    # today, we have only 1 complexity rule
    # password needs to be at least 6 chars long
    if len(password) < MIN_PASSWORD_LENGTH:
        return ComplexityError.MinLengthErr
    return ComplexityError.NoErr

