import re
from werkzeug.security import check_password_hash
from ecinema.data.ValidationData import (
    is_new_email, is_unique_username,
    is_active_user
)

'''
Place any code for validating user input here
Anywhere in the code base can access these by using
from ecinema.tools.validation import validateEmail, etc
'''


def validate_email(email: str) -> bool:
    return re.match(
        '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*'
        '@'
        '(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
        email) is not None


def validate_unique_email(email: str) -> bool:
    return is_new_email(email)


def validate_name(name: str) -> bool:
    return len(name) > 1 and len(name) < 100


def validate_password(password: str, confirmation: str) -> bool:
    return (password == confirmation and len(password) >= 8 and
            bool(re.search(r'\d', password)) and
            any(char.isupper() for char in password))


def validate_username(username: str) -> bool:
    return is_unique_username(username)


def validate_user_status(email: str) -> bool:
    return is_active_user(email)
